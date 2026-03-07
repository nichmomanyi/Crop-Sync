from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def run_comprehensive_recommendations(tx):
    # List of all TPEs
    tpes = ['ARID', 'SEMI_ARID', 'SUB_HUMID', 'HUMID', 'HIGH_ALTITUDE', 'LOWLAND_TROPICAL']

    for tpe in tpes:
        # Query 1: Recommend varieties with desired traits for the current TPE
        result = tx.run("""
        MATCH (tpe:TPE {name: $tpe_name})
        MATCH (v:Variety)-[:SUITABLE_FOR_TPE]->(tpe)
        MATCH (v)-[:HAS_TRAIT]->(t:Trait {type: 'Desired'})
        RETURN v.name AS Variety, collect(t.name) AS DesiredTraits, tpe.name AS TPE;
        """, tpe_name=tpe)
        print(f"\nRecommendations for {tpe} TPE with Desired Traits:")
        for record in result:
            print(record)

        # Query 2: Exclude varieties with negative traits for the current TPE
        result = tx.run("""
        MATCH (tpe:TPE {name: $tpe_name})
        MATCH (v:Variety)-[:SUITABLE_FOR_TPE]->(tpe)
        WHERE NOT EXISTS {
          MATCH (v)-[:HAS_TRAIT]->(t:Trait {type: 'Negative'})
        }
        RETURN v.name AS Variety, tpe.name AS TPE;
        """, tpe_name=tpe)
        print(f"\nRecommendations for {tpe} TPE excluding Negative Traits:")
        for record in result:
            print(record)

        # Query 3: Prioritize varieties with positive traits for the current TPE
        result = tx.run("""
        MATCH (tpe:TPE {name: $tpe_name})
        MATCH (v:Variety)-[:SUITABLE_FOR_TPE]->(tpe)
        MATCH (v)-[:HAS_TRAIT]->(t:Trait {type: 'Positive'})
        RETURN v.name AS Variety, collect(t.name) AS PositiveTraits, tpe.name AS TPE;
        """, tpe_name=tpe)
        print(f"\nRecommendations for {tpe} TPE with Positive Traits:")
        for record in result:
            print(record)

        # Query 4: Include weather data in recommendations for the current TPE
        result = tx.run("""
        MATCH (l:Location)-[:HAS_WEATHER]->(w:Weather {month: 'January', year: 2025})
        MATCH (l)<-[:FROM_COUNTRY]-(v:Variety)-[:SUITABLE_FOR_TPE]->(tpe:TPE {name: $tpe_name})
        MATCH (v)-[:HAS_TRAIT]->(t:Trait {type: 'Desired'})
        WHERE w.temperature > 25 AND w.rainfall < 100
        RETURN v.name AS Variety, collect(t.name) AS DesiredTraits, tpe.name AS TPE, l.name AS Location;
        """, tpe_name=tpe)
        print(f"\nRecommendations for {tpe} TPE with January 2025 Weather Conditions and Desired Traits:")
        for record in result:
            print(record)

# Execute comprehensive recommendations
with driver.session() as session:
    session.execute_read(run_comprehensive_recommendations)
