from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def link_weather_to_traits(tx):
    # Link weather conditions to positive traits
    tx.run("""
    MATCH (w:Weather)-[:BELONGS_TO_TPE]->(tpe:TPE)
    MATCH (l:Location)-[:HAS_WEATHER]->(w)
    MATCH (v:Variety)-[:FROM_COUNTRY]->(l)
    MATCH (v)-[:HAS_TRAIT]->(t:Trait {type: 'Positive'})
    MERGE (w)-[:PROMOTES_TRAIT]->(t)
    """)

    # Link weather conditions to negative traits
    tx.run("""
    MATCH (w:Weather)-[:BELONGS_TO_TPE]->(tpe:TPE)
    MATCH (l:Location)-[:HAS_WEATHER]->(w)
    MATCH (v:Variety)-[:FROM_COUNTRY]->(l)
    MATCH (v)-[:HAS_TRAIT]->(t:Trait {type: 'Negative'})
    MERGE (w)-[:LEADS_TO_TRAIT]->(t)
    """)

# Execute
with driver.session() as session:
    session.execute_write(link_weather_to_traits)

print("Weather conditions linked to traits in Neo4j!")
