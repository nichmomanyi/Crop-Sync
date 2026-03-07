import pandas as pd
import re

# Load the Excel file
file_path = './data_raw/Sorghum Crop Characteristics updated.xlsx'
sorghum_df = pd.read_excel(file_path, sheet_name='Sheet1')

# Clean column names
sorghum_df.columns = sorghum_df.columns.str.replace(r'[\u200b\s]+', '', regex=True)

# Clean variety names and create 'Variety with Year'
sorghum_df['Variety'] = sorghum_df['Varietyname'].str.replace(r'[\u200b\s]+', '', regex=True)
sorghum_df['YearofRelease'] = sorghum_df['YearofRelease'].astype(str).str.replace(r'[\u200b\s]+', '', regex=True)
sorghum_df['Variety with Year'] = sorghum_df['Variety'] + '(' + sorghum_df['YearofRelease'] + ')'

# Function to clean trait names
def clean_trait(trait_str):
    if pd.isna(trait_str):
        return []
    traits = trait_str.split(',')
    cleaned_traits = []
    for trait in traits:
        trait = re.sub(r'[\s\u200b\u000b]+', ' ', trait).strip()
        trait = trait.upper().replace(' ', '_')
        cleaned_traits.append(trait)
    return cleaned_traits

# Prepare a list to store variety-trait relationships
variety_trait_data = []

# Process each row in the dataframe
for _, row in sorghum_df.iterrows():
    variety = row['Variety with Year']
    country = row['Country']

    # Process positive traits
    positive_traits = clean_trait(row['Positivecharacteristics'])
    for trait in positive_traits:
        variety_trait_data.append({'Variety': variety, 'Trait': trait, 'Trait Type': 'Positive', 'Country': country})

    # Process negative traits
    negative_traits = clean_trait(row['Negativecharacteristics'])
    for trait in negative_traits:
        variety_trait_data.append({'Variety': variety, 'Trait': trait, 'Trait Type': 'Negative', 'Country': country})

    # Process desired traits
    desired_traits = clean_trait(row['Desiredcharacteristics'])
    for trait in desired_traits:
        variety_trait_data.append({'Variety': variety, 'Trait': trait, 'Trait Type': 'Desired', 'Country': country})

# Convert the list to a DataFrame
variety_trait_df = pd.DataFrame(variety_trait_data)

# Save the variety-trait relationships to a new CSV file
variety_trait_path = './data_processed/cleaned_sorghum_data.csv'
variety_trait_df.to_csv(variety_trait_path, index=False)

print(f"Variety-trait relationships with regions saved to {variety_trait_path}")
