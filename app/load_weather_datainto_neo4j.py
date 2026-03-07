from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Load the weather data
weather_path = './data_processed/simulated_monthly_weather.csv'
weather_df = pd.read_csv(weather_path)

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_weather_data(tx):
    for _, row in weather_df.iterrows():
        country = row['country']
        town = row['town']
        year = row['year']
        month = row['month']
        temperature = row['temperature']
        humidity = row['humidity']
        rainfall = row['rainfall']
        condition = row['condition']

        # Create Location node
        tx.run("""
        MERGE (l:Location {name: $name, country: $country, town: $town})
        """, name=f"{town}, {country}", country=country, town=town)

        # Create Weather node
        tx.run("""
        MERGE (w:Weather {
            country: $country,
            town: $town,
            year: $year,
            month: $month,
            temperature: $temperature,
            humidity: $humidity,
            rainfall: $rainfall,
            condition: $condition
        })
        """, country=country, town=town, year=year, month=month, temperature=temperature,
           humidity=humidity, rainfall=rainfall, condition=condition)

        # Create relationship between Location and Weather
        tx.run("""
        MATCH (l:Location {name: $name})
        MATCH (w:Weather {country: $country, town: $town, year: $year, month: $month})
        MERGE (l)-[:HAS_WEATHER]->(w)
        """, name=f"{town}, {country}", country=country, town=town, year=year, month=month)

# Execute
with driver.session() as session:
    session.execute_write(load_weather_data)

print("Weather data loaded into Neo4j!")
