from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254" 

# Load the TPEs
tpe_path = './data_processed/tpes.csv'
tpe_df = pd.read_csv(tpe_path)

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_tpes(tx):
    for _, row in tpe_df.iterrows():
        tpe_name = row['name']
        tpe_description = row['description']
        stressors = eval(row['stressors'])

        # Create TPE node
        tx.run("""
        MERGE (tpe:TPE {name: $name, description: $description})
        """, name=tpe_name, description=tpe_description)

        # Create stressor nodes and relationships
        for stressor in stressors:
            tx.run("""
            MERGE (s:Stressor {name: $name})
            """, name=stressor)

            tx.run("""
            MATCH (tpe:TPE {name: $tpe_name})
            MATCH (s:Stressor {name: $stressor_name})
            MERGE (tpe)-[:HAS_STRESSOR]->(s)
            """, tpe_name=tpe_name, stressor_name=stressor)

# Execute
with driver.session() as session:
    session.execute_write(load_tpes)

print("TPEs loaded into Neo4j!")
