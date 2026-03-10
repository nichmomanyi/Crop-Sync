from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_from_country_relationships(tx):
    # Create FROM_COUNTRY relationships
    result = tx.run("""
    MATCH (v:Variety), (c:Country)
    WHERE v.origin IS NOT NULL AND v.origin = c.name
    MERGE (v)-[:FROM_COUNTRY]->(c)
    RETURN v.name AS Variety, c.name AS Country;
    """)
    relationships = [dict(record) for record in result]
    print("FROM_COUNTRY Relationships Created:")
    for rel in relationships:
        print(rel)

with driver.session() as session:
    session.execute_write(create_from_country_relationships)
