from neo4j import GraphDatabase
import pandas as pd
import numpy as np

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Load the cleaned sorghum data
sorghum_path = './data_processed/cleaned_sorghum_data.csv'
sorghum_df = pd.read_csv(sorghum_path)

# Drop rows with NaN values in critical columns
sorghum_df.dropna(subset=['Trait', 'Trait Type'], inplace=True)

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def update_traits(tx):
    for _, row in sorghum_df.iterrows():
        trait = row['Trait']
        trait_type = row['Trait Type']

        # Update Trait node with type
        tx.run("""
        MERGE (t:Trait {name: $name})
        SET t.type = $type
        """, name=trait, type=trait_type)

# Execute
with driver.session() as session:
    session.execute_write(update_traits)

print("Traits updated in Neo4j!")
