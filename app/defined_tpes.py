import pandas as pd
import os

# Define updated TPEs and their stressors
tpes = [
    {
        "name": "ARID",
        "description": "Extremely dry areas with minimal rainfall, often less than 400 mm annually",
        "stressors": ["DROUGHT", "HEAT", "STRIGA", "SALINITY"]
    },
    {
        "name": "SEMI_ARID",
        "description": "Areas with moderate rainfall (400-800 mm annually) but prone to drought",
        "stressors": ["DROUGHT", "HEAT", "STRIGA", "BIRD_DAMAGE"]
    },
    {
        "name": "SUB_HUMID",
        "description": "Areas with moderate to high rainfall (800-1200 mm annually)",
        "stressors": ["GRAIN_MOLD", "ANTHRACNOSE", "BIRD_DAMAGE", "PESTS"]
    },
    {
        "name": "HUMID",
        "description": "High rainfall areas with high humidity, often more than 1200 mm annually",
        "stressors": ["GRAIN_MOLD", "ANTHRACNOSE", "APHIDS", "FUNGAL_DISEASES"]
    },
    {
        "name": "HIGH_ALTITUDE",
        "description": "Cool, high-altitude areas, typically above 1500 meters",
        "stressors": ["COLD", "STRIGA", "LOW_OXYGEN"]
    },
    {
        "name": "LOWLAND_TROPICAL",
        "description": "Warm, low-altitude areas with consistent rainfall",
        "stressors": ["HIGH_HUMIDITY", "PESTS", "DISEASES"]
    }
]

# Create directory if it doesn't exist
os.makedirs('./data_processed', exist_ok=True)

# Save TPEs to a CSV file
tpe_df = pd.DataFrame(tpes)
tpe_path = './data_processed/tpes.csv'
tpe_df.to_csv(tpe_path, index=False)

print(f"Generalized TPEs saved to {tpe_path}")
