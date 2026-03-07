from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def classify_weather_data(tx):
    # Classify ARID
    tx.run("""
    MATCH (w:Weather)
    WHERE w.temperature > 30 AND w.rainfall < 50 AND w.tpe IS NULL
    SET w.tpe = 'ARID'
    """)

    # Classify SEMI_ARID
    tx.run("""
    MATCH (w:Weather)
    WHERE w.temperature > 25 AND w.rainfall < 100 AND w.tpe IS NULL
    SET w.tpe = 'SEMI_ARID'
    """)

    # Classify SUB_HUMID
    tx.run("""
    MATCH (w:Weather)
    WHERE w.temperature > 20 AND w.rainfall >= 100 AND w.rainfall <= 300 AND w.tpe IS NULL
    SET w.tpe = 'SUB_HUMID'
    """)

    # Classify HUMID
    tx.run("""
    MATCH (w:Weather)
    WHERE w.temperature > 18 AND w.rainfall > 300 AND w.tpe IS NULL
    SET w.tpe = 'HUMID'
    """)

    # Classify HIGH_ALTITUDE
    tx.run("""
    MATCH (w:Weather)
    WHERE w.temperature < 18 AND w.tpe IS NULL
    SET w.tpe = 'HIGH_ALTITUDE'
    """)

    # Classify LOWLAND_TROPICAL
    tx.run("""
    MATCH (w:Weather)
    WHERE w.temperature > 25 AND w.humidity > 70 AND w.tpe IS NULL
    SET w.tpe = 'LOWLAND_TROPICAL'
    """)

# Execute
with driver.session() as session:
    session.execute_write(classify_weather_data)

print("Weather data classified and updated in Neo4j!")
