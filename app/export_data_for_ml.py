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
    MATCH (v:Variety)-[:FROM_COUNTRY]->(c:Country)
    MATCH (v)-[:GROWN_IN]->(l:Location)
    MATCH (l)-[:HAS_WEATHER]->(w:Weather)
    MATCH (v)-[:HAS_TRAIT]->(t:Trait)
    RETURN l.name AS Location, v.name AS Variety, t.name AS Trait, t.type AS TraitType, w.tpe AS TPE,
           w.temperature AS Temperature, w.rainfall AS Rainfall, w.humidity AS Humidity
    LIMIT 1000;
    """)
    data = [dict(record) for record in result]
    return pd.DataFrame(data)

with driver.session() as session:
    df = session.execute_read(export_data_for_ml)

if not df.empty:
    df.to_csv('./data_processed/sorghum_ml_data.csv', index=False)
    print(f"Data exported to sorghum_ml_data.csv. Rows: {len(df)}")
else:
    print("No data returned. Check your query and data in Neo4j.")
