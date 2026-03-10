from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_grown_in_relationships(tx):
    # Create GROWN_IN relationships
    result = tx.run("""
    MATCH (v:Variety), (l:Location)
    WHERE v.location IS NOT NULL AND v.location = l.name
    MERGE (v)-[:GROWN_IN]->(l)
    RETURN v.name AS Variety, l.name AS Location;
    """)
    relationships = [dict(record) for record in result]
    print("GROWN_IN Relationships Created:")
    for rel in relationships:
        print(rel)

with driver.session() as session:
    session.execute_write(create_grown_in_relationships)
