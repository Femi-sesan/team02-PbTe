# Adaptive Power Textiles – Thermoelectric Module Web Application

## How to Run the Application

1. Open a terminal in the project root directory.
2. Install required packages (if not already installed):

   pip install streamlit numpy plotly

3. Run the application:

   streamlit run Home.py

The application will open in your browser automatically.

---

## Project Structure & Deliverables

**Home Page**
- Project overview and motivation.
- Navigation to all analytical and simulation sections.

**Science & Technology Pages**
- Thermoelectric principles.
- Material background and device architecture.

**Analysis Page (pages/4_Analytical_Analysis.py)**
Includes:
- Analytical derivation of thermoelectric couple equations (Voc, Rint, power vs load)
- Impedance matching demonstration (Rload ≈ Rint)
- ΔT² power scaling validation
- COMSOL comparison table
- Analytical vs COMSOL discrepancy discussion
- Database-based material pair selection rationale
- 5 V module sizing and smartphone charging estimate

**COMSOL Simulation Page**
- Numerical simulation results
- Extracted performance metrics
- Validation against analytical model

---

## Notes

- All analytical calculations use consistent representative material properties.
- COMSOL results are used as the higher-fidelity reference.
- Charging estimates include an adjustable system efficiency factor to reflect realistic power electronics losses.