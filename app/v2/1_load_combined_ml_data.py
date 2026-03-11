import psycopg2
import pandas as pd

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'cropsync',
    'user': 'postgres',
    'password': 'nichdee254',
    'port': '5432'
}
conn = psycopg2.connect(**db_params)

query = """
    SELECT * FROM cropsync_ml_data;
"""

ml_data = pd.read_sql(query, conn)

ml_data.to_csv('./data_processed/combined_ml_data.csv', index=False)

# Close the connection
conn.close()
print("Data successfully pulled and saved to combined_ml_data.csv")
