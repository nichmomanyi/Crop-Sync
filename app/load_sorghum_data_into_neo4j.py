from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Load the sorghum data
sorghum_path = './data_processed/cleaned_sorghum_data.csv'
sorghum_df = pd.read_csv(sorghum_path)

# Drop rows with NaN values in critical columns
sorghum_df.dropna(subset=['Variety', 'Trait', 'Trait Type', 'Country'], inplace=True)

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_sorghum_data(tx):
    for _, row in sorghum_df.iterrows():
        variety = row['Variety']
        trait = row['Trait']
        trait_type = row['Trait Type']
        country = row['Country']

        # Create Country node
        tx.run("MERGE (c:Country {name: $name})", name=country)

        # Create Variety node
        tx.run("MERGE (v:Variety {name: $name})", name=variety)

        # Create Trait node with type
        tx.run("MERGE (t:Trait {name: $name, type: $type})", name=trait, type=trait_type)

        # Create relationship between Variety and Country
        tx.run("""
        MATCH (v:Variety {name: $variety})
        MATCH (c:Country {name: $country})
        MERGE (v)-[:FROM_COUNTRY]->(c)
        """, variety=variety, country=country)

        # Create relationship between Variety and Trait
        tx.run("""
        MATCH (v:Variety {name: $variety})
        MATCH (t:Trait {name: $trait})
        MERGE (v)-[:HAS_TRAIT]->(t)
        """, variety=variety, trait=trait)

# Execute
with driver.session() as session:
    session.execute_write(load_sorghum_data)

print("Sorghum data loaded into Neo4j!")
