import psycopg2
import pandas as pd
import ast

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'cropsync',
    'user': 'postgres',
    'password': 'nichdee254',
    'port': '5432'
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Load CSV files
sorghum_df = pd.read_csv('./data_processed/cleaned_sorghum_data.csv')
weather_df = pd.read_csv('./data_processed/simulated_monthly_weather.csv')
tpes_df = pd.read_csv('./data_processed/tpes.csv')

# Convert stressors column to PostgreSQL array format
tpes_df['stressors'] = tpes_df['stressors'].apply(lambda x: '{' + ','.join([f'"{item.strip()}"' for item in ast.literal_eval(x)]) + '}')

# Function to insert data into a table
def insert_data(df, table_name, columns, unique_column=None):
    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(columns))
        if unique_column:
            query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT ({unique_column}) DO NOTHING
            """
        else:
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, tuple(row[col] for col in columns))
    conn.commit()

# Insert countries
unique_countries = pd.concat([
    sorghum_df[['Country']].rename(columns={'Country': 'name'}),
    weather_df[['country']].rename(columns={'country': 'name'})
]).drop_duplicates().dropna()

insert_data(unique_countries, 'countries', ['name'], unique_column='name')

# Extract unique locations
unique_locations = weather_df[['country', 'town', 'lat', 'lon']].drop_duplicates()

# Debug: Print countries in unique_locations
print("Countries in unique_locations:", unique_locations['country'].unique())

# Fetch country_id for each country
country_ids = {}
for country in unique_locations['country'].unique():
    cursor.execute("SELECT country_id FROM countries WHERE name = %s", (country,))
    result = cursor.fetchone()
    if result:
        country_ids[country] = result[0]
    else:
        print(f"Country '{country}' not found in the countries table.")

unique_locations['country_id'] = unique_locations['country'].map(country_ids)

# Drop rows with missing country_id
unique_locations = unique_locations.dropna(subset=['country_id'])

# Insert locations with unique constraint
insert_data(unique_locations, 'locations', ['country_id', 'town', 'lat', 'lon'], unique_column='town, country_id')

# Insert tpes
insert_data(tpes_df, 'tpes', ['name', 'description', 'stressors'], unique_column='name')

# Insert crops
cursor.execute("""
    INSERT INTO crops (name)
    VALUES ('sorghum')
    ON CONFLICT (name) DO NOTHING
""")
conn.commit()

# Insert traits
unique_traits = sorghum_df[['Trait', 'Trait Type']].rename(columns={'Trait': 'name', 'Trait Type': 'trait_type'}).drop_duplicates()
insert_data(unique_traits, 'traits', ['name', 'trait_type'], unique_column='name')

# Insert varieties
unique_varieties = sorghum_df[['Variety']].rename(columns={'Variety': 'name'}).drop_duplicates()
unique_varieties['crop_id'] = 1  # Assuming crop_id for sorghum is 1
insert_data(unique_varieties, 'varieties', ['crop_id', 'name'], unique_column='crop_id, name')

# Insert variety_traits
variety_traits = sorghum_df[['Variety', 'Trait']].drop_duplicates()

# Fetch variety_id for each variety
variety_ids = {}
for variety in variety_traits['Variety'].unique():
    cursor.execute("SELECT variety_id FROM varieties WHERE name = %s", (variety,))
    result = cursor.fetchone()
    if result:
        variety_ids[variety] = result[0]
    else:
        print(f"Variety '{variety}' not found in the varieties table.")

variety_traits['variety_id'] = variety_traits['Variety'].map(variety_ids)

# Fetch trait_id for each trait
trait_ids = {}
for trait in variety_traits['Trait'].unique():
    cursor.execute("SELECT trait_id FROM traits WHERE name = %s", (trait,))
    result = cursor.fetchone()
    if result:
        trait_ids[trait] = result[0]
    else:
        print(f"Trait '{trait}' not found in the traits table.")

variety_traits['trait_id'] = variety_traits['Trait'].map(trait_ids)

# Drop rows with missing variety_id or trait_id
variety_traits = variety_traits.dropna(subset=['variety_id', 'trait_id'])

# Insert variety_traits with unique constraint
insert_data(variety_traits, 'variety_traits', ['variety_id', 'trait_id'], unique_column='variety_id, trait_id')

# Insert weather
def get_location_id(row):
    cursor.execute(
        "SELECT location_id FROM locations WHERE country_id = (SELECT country_id FROM countries WHERE name = %s) AND town = %s",
        (row['country'], row['town'])
    )
    result = cursor.fetchone()
    return result[0] if result else None

weather_df['location_id'] = weather_df.apply(get_location_id, axis=1)

# Drop rows with missing location_id
weather_df = weather_df.dropna(subset=['location_id'])

insert_data(weather_df, 'weather', ['location_id', 'year', 'month', 'temperature', 'humidity', 'condition', 'rainfall'])

# Close connection
cursor.close()
conn.close()