from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def check_nodes(tx):
    # Check Variety nodes
    result = tx.run("MATCH (v:Variety) RETURN v.name AS Variety LIMIT 10;")
    varieties = [record["Variety"] for record in result]
    print("Variety Nodes:", varieties)

    # Check Country nodes
    result = tx.run("MATCH (c:Country) RETURN c.name AS Country LIMIT 10;")
    countries = [record["Country"] for record in result]
    print("Country Nodes:", countries)

    # Check Location nodes
    result = tx.run("MATCH (l:Location) RETURN l.name AS Location LIMIT 10;")
    locations = [record["Location"] for record in result]
    print("Location Nodes:", locations)

    # Check Trait nodes
    result = tx.run("MATCH (t:Trait) RETURN t.name AS Trait LIMIT 10;")
    traits = [record["Trait"] for record in result]
    print("Trait Nodes:", traits)

    # Check Weather nodes
    result = tx.run("MATCH (w:Weather) RETURN w LIMIT 10;")
    weather = [dict(record["w"]) for record in result]
    print("Weather Nodes:", weather)

with driver.session() as session:
    session.execute_read(check_nodes)
