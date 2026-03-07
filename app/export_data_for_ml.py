from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def export_data_for_ml(tx):
    result = tx.run("""
    MATCH (l:Location)-[:HAS_WEATHER]->(w:Weather)
    MATCH (v:Variety)-[:FROM_COUNTRY]->(l)
    MATCH (v)-[:HAS_TRAIT]->(t:Trait)
    RETURN l.name AS Location, v.name AS Variety, t.name AS Trait, t.type AS TraitType, w.tpe AS TPE,
           w.temperature AS Temperature, w.rainfall AS Rainfall, w.humidity AS Humidity;
    """)
    data = [dict(record) for record in result]
    return pd.DataFrame(data)

# Execute
with driver.session() as session:
    df = session.execute_read(export_data_for_ml)

# Save to CSV
df.to_csv('./data_processed/sorghum_ml_data.csv', index=False)
print("Data exported for ML to sorghum_ml_data.csv")
