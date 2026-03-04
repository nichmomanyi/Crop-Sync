# CropSync TPP Builder (Sorghum MVP) 🌾
A lightweight, explainable **Target Product Profile (TPP)** builder for sorghum breeding programs using a **Neo4j Knowledge Graph + Machine Learning** approach.

This MVP helps translate crop characteristic evidence (positive/negative/desired traits) into a **breeder-ready TPP**, aligned to simplified **Target Populations of Environments (TPEs)** (e.g., hot-dry, Striga-prone, humid/mold-risk).

---

## Why this project?
Breeding decisions often struggle with:
- unclear or inconsistent trait definitions (free text),
- weak traceability for “why” a trait is prioritized,
- climate and soil stress variability across target zones.

CropSync addresses this by:
- standardizing trait phrases into reusable tags (Trait Dictionary),
- storing trait evidence and relationships in Neo4j for explainability,
- ranking TPP traits using a simple, scalable scoring approach.

---

## MVP Features
✅ Extracts trait signals from an Excel crop-characteristics sheet  
✅ Builds a **Trait Dictionary v1** (raw phrases → standardized tags)  
✅ Loads trait nodes into **Neo4j** (with evidence phrases)  
✅ Generates a **TPP v1** (must-have / preferred / avoid) for sorghum  
✅ (Optional) Streamlit UI to interactively generate and export TPPs

---

## Tech Stack
- **Neo4j** (Knowledge Graph / Explainability)
- **Python** (Pandas, Neo4j driver)
- **Streamlit** (simple UI)
- **Scikit-learn** (ML-lite components; scalable later)

---

## Project Structure
