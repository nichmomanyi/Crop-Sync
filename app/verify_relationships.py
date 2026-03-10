from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def verify_relationships(tx):
    # Verify FROM_COUNTRY relationships
    result = tx.run("""
    MATCH (v:Variety)-[:FROM_COUNTRY]->(c:Country)
    RETURN v.name AS Variety, c.name AS Country
    LIMIT 10;
    """)
    from_country_rels = [dict(record) for record in result]
    print("FROM_COUNTRY Relationships:")
    for rel in from_country_rels:
        print(rel)

    # Verify GROWN_IN relationships
    result = tx.run("""
    MATCH (v:Variety)-[:GROWN_IN]->(l:Location)
    RETURN v.name AS Variety, l.name AS Location
    LIMIT 10;
    """)
    grown_in_rels = [dict(record) for record in result]
    print("\nGROWN_IN Relationships:")
    for rel in grown_in_rels:
        print(rel)

with driver.session() as session:
    session.execute_read(verify_relationships)
