from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "nichdee254"  # Replace with your actual password

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def link_varieties_to_tpes(tx):
    # Link varieties with drought-tolerant traits to ARID TPE
    tx.run("""
    MATCH (v:Variety)-[:HAS_TRAIT]->(t:Trait)
    WHERE t.name IN ['DROUGHT_TOLERANT', 'HEAT_TOLERANT']
    MATCH (tpe:TPE {name: 'ARID'})
    MERGE (v)-[:SUITABLE_FOR_TPE]->(tpe)
    """)

    # Link varieties with grain mold resistance to HUMID TPE
    tx.run("""
    MATCH (v:Variety)-[:HAS_TRAIT]->(t:Trait)
    WHERE t.name IN ['GRAIN_MOLD_RESISTANT', 'FUNGAL_DISEASE_RESISTANT']
    MATCH (tpe:TPE {name: 'HUMID'})
    MERGE (v)-[:SUITABLE_FOR_TPE]->(tpe)
    """)

    # Link varieties with pest resistance to SUB_HUMID TPE
    tx.run("""
    MATCH (v:Variety)-[:HAS_TRAIT]->(t:Trait)
    WHERE t.name IN ['PEST_RESISTANT']
    MATCH (tpe:TPE {name: 'SUB_HUMID'})
    MERGE (v)-[:SUITABLE_FOR_TPE]->(tpe)
    """)

    # Link varieties with cold tolerance to HIGH_ALTITUDE TPE
    tx.run("""
    MATCH (v:Variety)-[:HAS_TRAIT]->(t:Trait)
    WHERE t.name IN ['COLD_TOLERANT']
    MATCH (tpe:TPE {name: 'HIGH_ALTITUDE'})
    MERGE (v)-[:SUITABLE_FOR_TPE]->(tpe)
    """)

    # Link varieties with disease resistance to LOWLAND_TROPICAL TPE
    tx.run("""
    MATCH (v:Variety)-[:HAS_TRAIT]->(t:Trait)
    WHERE t.name IN ['DISEASE_RESISTANT']
    MATCH (tpe:TPE {name: 'LOWLAND_TROPICAL'})
    MERGE (v)-[:SUITABLE_FOR_TPE]->(tpe)
    """)

# Execute
with driver.session() as session:
    session.execute_write(link_varieties_to_tpes)

print("Varieties linked to TPEs in Neo4j!")
