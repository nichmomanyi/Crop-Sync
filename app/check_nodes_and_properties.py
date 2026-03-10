from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def check_nodes_and_properties(tx):
    # Check Variety nodes and their properties
    result = tx.run("""
    MATCH (v:Variety)
    RETURN v.name AS Variety, keys(v) AS Properties, properties(v) AS PropertyValues
    LIMIT 10;
    """)
    varieties = [dict(record) for record in result]
    print("Variety Nodes and Properties:")
    for variety in varieties:
        print(variety)

    # Check Country nodes
    result = tx.run("""
    MATCH (c:Country)
    RETURN c.name AS Country
    LIMIT 10;
    """)
    countries = [dict(record) for record in result]
    print("\nCountry Nodes:")
    for country in countries:
        print(country)

    # Check Location nodes
    result = tx.run("""
    MATCH (l:Location)
    RETURN l.name AS Location
    LIMIT 10;
    """)
    locations = [dict(record) for record in result]
    print("\nLocation Nodes:")
    for location in locations:
        print(location)

    # Check Trait nodes
    result = tx.run("""
    MATCH (t:Trait)
    RETURN t.name AS Trait, t.type AS TraitType
    LIMIT 10;
    """)
    traits = [dict(record) for record in result]
    print("\nTrait Nodes:")
    for trait in traits:
        print(trait)

    # Check Weather nodes
    result = tx.run("""
    MATCH (w:Weather)
    RETURN w
    LIMIT 10;
    """)
    weather = [dict(record) for record in result]
    print("\nWeather Nodes:")
    for w in weather:
        print(w)

with driver.session() as session:
    session.execute_read(check_nodes_and_properties)
