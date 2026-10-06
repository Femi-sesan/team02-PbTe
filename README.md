# Project Template (2025)

Welcome to your team's project repository!

Each team will complete the following parts:
1. **Analytical modeling** of the thermoelectric device (Part 2A)
2. **COMSOL simulation** and comparison (Part 2B)
3. **Promotional video** to attract funding (Part 3)
4. **AI-based material selection** (Part 4)

The final deliverable is a **Streamlit website** that summarizes your work for a general scientific audience.

---

## 🧱 Folder structure
```bash
project-template/
│
├── streamlit_app/
│ ├── app.py # Streamlit app entry point
│ ├── pages/ # optional extra pages
│ └── assets/ # figures, video, etc.
│
├── notebooks/
│ ├── analytical_model.ipynb
│ ├── comsol_postprocessing.ipynb
│ └── ai_material_selection.ipynb
│
├── data/
│ ├── material_properties.csv
│ └── comsol_results/
│
├── README.md
└── requirements.txt

---

## 🚀 How to run your Streamlit app locally

1. Make sure you have **Python ≥ 3.10** installed.  
2. Open a terminal and type:

```bash
git clone <your-team-repo-url>
cd <your-team-repo>
pip install -r requirements.txt
streamlit run streamlit_app/app.py


Then open the local link (usually http://localhost:8501)

---
