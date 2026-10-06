import os
import base64
import numpy as np

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import py3Dmol

from theme import apply_global_background

# --- Page Configuration ---
st.set_page_config(page_title="Technology - APT", page_icon="🔬", layout="wide")

# --- Background ---
apply_global_background(os.path.join("PROJECT IMG", "Hero_background.png"), height_px=1200)

# --- HELPER: PROJECT ROOT ---
def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ROOT_DIR = project_root()
PROJECT_IMG_DIR = os.path.join(ROOT_DIR, "PROJECT IMG")

# --- UNIVERSAL HEADER FUNCTION ---
def render_header():
    st.markdown("""
        <style>
            /* 1. HIDE DEFAULT STREAMLIT HEADER */
            header[data-testid="stHeader"] {
                display: none;
            }

            /* 2. MAIN CONTENT PADDING */
            .block-container { 
                padding-top: 150px !important; 
                padding-bottom: 2rem; 
            }
            
            /* 3. SAFE FIXED HEADER CONTAINER */
            div[data-testid="stHorizontalBlock"]:has(#fixed-header-marker) {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                z-index: 999999;
                background-color: white; 
                border-bottom: 1px solid #e0e0e0;
                padding-top: 1.5rem; 
                padding-bottom: 1.5rem; 
                padding-left: 3rem;
                padding-right: 3rem;
                height: auto; 
                min-height: 100px; 
                align-items: center; 
            }
            
            /* 4. LOGO SIZING */
            div[data-testid="stHorizontalBlock"]:has(#fixed-header-marker) img {
                object-fit: contain !important;
                margin-bottom: 0px !important;
                max-height: 45px !important; 
            }
        </style>
    """, unsafe_allow_html=True)

    col_logos, col_nav = st.columns([1.2, 3.8])
    
    with col_logos:
        st.markdown('<div id="fixed-header-marker" style="display:none;"></div>', unsafe_allow_html=True)
        try:
            st.image(os.path.join(PROJECT_IMG_DIR, "Program_logo.png"), width=85)
        except Exception:
            st.write("⚡ FAME AIS")
        try:
            st.image(os.path.join(PROJECT_IMG_DIR, "Team_logo.png"), width=85)
        except Exception:
            st.write("⚡ PbTe Ligence")
    
    with col_nav:
        nav1, nav2, nav3, nav4, nav5, nav6, nav7 = st.columns(7)
        with nav1: st.page_link("Home.py", label="Home", icon="🏠")
        with nav2: st.page_link("pages/1_About_Us.py", label="About", icon="👥")
        with nav3: st.page_link("pages/2_The_Science.py", label="Science", icon="⚛️")
        with nav4: st.page_link("pages/3_The_Technology.py", label="Tech", icon="🔬")
        with nav5: st.page_link("pages/4_Analytical_Analysis.py", label="Analysis", icon="📈")
        with nav6: st.page_link("pages/5_COMSOL_Simulation.py", label="COMSOL", icon="🖥️")
        with nav7: st.page_link("pages/6_AI_Material_Selection.py", label="AI/ML", icon="🤖")

render_header()

# --- Global CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, li {
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stSidebar"] { top: 100px !important; height: calc(100vh - 100px) !important; }
    [data-testid="collapsedControl"] { top: 100px !important; }

    h1, h2, h3 { color: #000000; }

    .ds-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.90rem;
        margin-bottom: 16px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        background: white;
        table-layout: fixed;
    }

    .ds-table th, .ds-table td {
        border: 1px solid #ddd;
        padding: 8px 12px;
        text-align: left;
        vertical-align: top;
        line-height: 1.45;
    }

    .ds-table th {
        background-color: #e3f2fd;
        color: #333;
        width: 25%;
        font-weight: 600;
    }

    .ds-table td { 
        color: #444;
        word-wrap: break-word;
    }

    .ds-table small {
        display: block;
        font-size: 0.78rem;
        color: #666;
        margin-top: 2px;
        line-height: 1.35;
    }

    .ds-notes {
        background-color: #f9f9f9;
        border-left: 4px solid #000000;
        padding: 15px;
        margin-top: 10px;
        font-size: 0.95rem;
        color: #444;
    }

    .model-card {
        background: white;
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 14px 14px 10px 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        text-align: center;
    }

    .model-title {
        font-weight: 700;
        margin: 0 0 4px 0;
        font-size: 1.05rem;
        color: #111;
    }

    .model-sub {
        margin: 0 0 10px 0;
        color: #6b7280;
        font-size: 0.92rem;
    }

    .compact-head {
        background-color:#007BFF !important;
        color:white !important;
        text-align:center !important;
        padding:10px 12px !important;
        font-weight:700;
    }

    .center-block {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Datasheet CSV Download ---
csv_content = """Property,Value,Unit
Material Name,Lead Telluride,PbTe
Band Gap,0.81,eV (Calculated)
Crystal Structure,Rock Salt (Halite),Fm-3m
Lattice Parameter,6.54,Å
Density,7.94,g/cm³
Formation Energy,-0.504,eV/atom
Bulk Modulus,38,GPa
Shear Modulus,24,GPa
Poisson's Ratio,0.24,-
Suggested Substrate,ZnTe / SiC / InAs,-
"""

col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("Lead Telluride (PbTe)")
    st.caption("Technical Data Sheet | Revision 2026")
with col_btn:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.download_button("📥 Download Datasheet (CSV)", csv_content, "PbTe_Datasheet.csv", "text/csv")

st.divider()

# --- Section 1: Material ID ---
st.subheader("Material Identification")
st.markdown("The following table summarizes the essential identification details of Lead Telluride (PbTe):")

mi_col1, mi_col2 = st.columns([1.3, 1], gap="large", vertical_alignment="center")

with mi_col1:
    st.markdown(
        """
        <table class="ds-table">
            <tr><th>Material Name</th><td>Lead Telluride</td></tr>
            <tr><th>Chemical Formula</th><td>PbTe</td></tr>
            <tr><th>Category</th><td><b>Narrow-gap Semiconductor</b></td></tr>
            <tr><th>Type</th><td><b>n-type or p-type</b> (via doping)</td></tr>
            <tr><th>Space Group</th><td>Fm-3m (Number 225)</td></tr>
            <tr><th>Band Gap</th><td>0.81 eV (Direct)</td></tr>
            <tr><th>Density</th><td>7.94 g/cm³</td></tr>
        </table>
        """,
        unsafe_allow_html=True,
    )

# --- Section 2: Crystal Info ---
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Crystal & Structural Information")

top_left, top_right = st.columns([1, 1], gap="large", vertical_alignment="center")

with top_left:
    st.markdown('<div class="center-block">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="width:100%; max-width:600px;">
            <table class="ds-table">
                <tr><th>Crystal Structure</th><td><b>Face-Centered Cubic (FCC)</b></td></tr>
                <tr><th>Space Group</th><td>Fm-3m (225) - Rock Salt Type</td></tr>
                <tr><th>Lattice Parameter</th><td>6.54 Å</td></tr>
                <tr><th>Anions (Te)</th><td>Face-centered lattice (0,0,0)</td></tr>
                <tr><th>Cations (Pb)</th><td>Octahedral sites (½,½,½)</td></tr>
                <tr><th>Bond Length</th><td>3.27 Å (Pb–Te)</td></tr>
                <tr><th>Density</th><td>7.94 g/cm³</td></tr>
            </table>
            <div class="ds-notes">
                <b>Note:</b> PbTe crystallizes in a rock-salt structure with alternating Pb and Te atoms in a cubic lattice.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with top_right:
    st.markdown('<div class="center-block">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="width:100%; max-width:600px;">
            <div class="model-card">
                <div class="model-title">3D Model (GLB)</div>
                <div class="model-sub">Interactive rendering of the PbTe crystal structure.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    glb_path = os.path.join(PROJECT_IMG_DIR, "pbte_structure.glb")

    if not os.path.exists(glb_path):
        st.warning(f"GLB file not found here: {glb_path}")
    else:
        with open(glb_path, "rb") as f:
            glb_b64 = base64.b64encode(f.read()).decode()

        components.html(
            f"""
            <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
            <div style="margin-top:10px; display:flex; justify-content:center; align-items:center; width:100%;">
              <model-viewer
                  src="data:model/gltf-binary;base64,{glb_b64}"
                  alt="PbTe 3D Structure"
                  auto-rotate
                  camera-controls
                  shadow-intensity="0.6"
                  style="width: 100%; max-width: 600px; height: 380px; background: white; border: 1px solid #eee; border-radius: 12px;">
              </model-viewer>
            </div>
            """,
            height=410,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- Section 3: Thermoelectrical ---
st.subheader("Thermoelectrical Properties")
st.markdown("""
<table class="ds-table">
    <thead>
        <tr><th colspan="4" class="compact-head">Thermoelectric Properties</th></tr>
    </thead>
    <tbody>
        <tr>
            <th>Melting Temperature</th>
            <td>1197 K</td>
            <th>Thermal Conductivity</th>
            <td>1.46 W/m·K</td>
        </tr>
        <tr>
            <th>Carrier Concentration Order</th>
            <td>~10<sup>19</sup> cm<sup>−3</sup></td>
            <th>Figure of Merit (zT)</th>
            <td><b>zTmax ≥ 2</b> in p-type<br><b>zTmax ≈ 1.8</b> in n-type</td>
        </tr>
        <tr>
            <th>Seebeck Coefficient</th>
            <td>
                -187 μV/K <small>undoped PbTe</small>
                -200 μV/K <small>Iodine doped PbTe (n-type)</small>
                +240 μV/K <small>Sodium doped PbTe (p-type)</small>
            </td>
            <th>Temperature Working Range</th>
            <td><b>500 – 800 K</b></td>
        </tr>
        <tr>
            <th>Electrical Conductivity</th>
            <td>
                60.976 × 10<sup>3</sup> S/m <small>undoped PbTe</small>
                100.0 × 10<sup>3</sup> S/m <small>Iodine doped PbTe (n-type)</small>
                90.0 × 10<sup>3</sup> S/m <small>Sodium doped PbTe (p-type)</small>
            </td>
            <th>Application Window</th>
            <td>Mid-to-high temperature thermoelectric conversion</td>
        </tr>
    </tbody>
</table>
<div class="ds-notes">
    <p>➤ <b>Seebeck Values:</b> Considered high for a thermoelectric semiconductor.</p>
    <p>➤ <b>Figure of Merit (zT):</b> We utilize nanostructuring to lower the lattice thermal conductivity, pushing zT higher than bulk values.</p>
    <p>➤ <b>Operating Window:</b> PbTe is optimal for mid-to-high temperature waste heat recovery.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Section 4: Mechanical ---
st.subheader("Mechanical Properties (Elastic Tensor)")
st.markdown("""
<table class="ds-table">
    <tr><th>Bulk Modulus (Voigt-Reuss-Hill)</th><td>38 GPa</td><th>Shear Modulus</th><td>24 GPa</td></tr>
    <tr><th>Young’s Modulus</th><td>~50 GPa</td><th>Poisson’s Ratio</th><td>0.24</td></tr>
</table>
<div class="ds-notes">
    <b>Analysis:</b> The low Shear Modulus (24 GPa) indicates that PbTe is mechanically soft and brittle. 
    In the device design, we must minimize thermal stress to prevent cracking.
</div>
""", unsafe_allow_html=True)

st.divider()

# --- NEW SECTION: MODULE ASSEMBLY (CORRECTED & PROFESSIONAL) ---
st.subheader("Thermoelectric Module Assembly")
st.write("To construct a functional generator, the material architecture must allow for series electrical connection and parallel thermal flow.")

# --- Doping Explanation Box (PROFESSIONAL) ---
st.info("""
**Thermoelectric Couple Architecture**
- **N-type leg:** PbTe doped to supply electrons as charge carriers.
- **P-type leg:** PbTe doped to supply holes as charge carriers.
"""
)

mod_col1, mod_col2 = st.columns(2, gap="large")

with mod_col1:
    st.markdown("#### Counterpart Selection")
    st.write("Optimization of the p-type partner for our n-type PbTe leg:")
    
    counterpart = st.selectbox(
        "Select counterpart configuration:",
        ["PbTe (p-type doped)", "TAGS-85 (p-type)", "Bi2Te3 (Low Temp)"],
        index=0,
    )

    if counterpart == "PbTe (p-type doped)":
        st.success(
            "Using PbTe for both legs reduces thermal expansion mismatch and improves mechanical reliability."
        )
    elif counterpart == "TAGS-85 (p-type)":
        st.warning(
            "TAGS-85 can be effective, but may introduce thermal stress due to different expansion behavior."
        )
    else:
        st.error(
            "Bi2Te3 is designed for lower temperatures and is not suitable for PbTe operating temperatures."
        )

with mod_col2:
    st.markdown("#### Substrate Compatibility")
    st.write("Analysis of substrate lattice parameters vs. PbTe ($a = 6.54 \\AA$) to ensure epitaxial growth and mechanical adhesion:")
    
    substrate = st.radio("Select Substrate Material:", ["ZnTe (Zinc Telluride)", "SiC (Silicon Carbide)", "InAs (Indium Arsenide)"])
    
    st.caption(f"**Analysis:** {substrate} provides the necessary electrical insulation and mechanical support. Its selection is based on minimizing lattice mismatch to reduce interface defects.")

st.divider()

# --- Section 5: Graph ---
st.subheader("Performance Graph")
# Real zT values computed from PbTe transport properties (temperature-dependent model)
temp_x  = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]
zT_n_data = [0.462, 0.576, 0.699, 0.829, 0.965, 1.104, 1.246, 1.388, 1.529, 1.667, 1.8]   # n-type (I-doped)
zT_p_data = [0.599, 0.749, 0.909, 1.079, 1.257, 1.439, 1.624, 1.809, 1.992, 2.171, 2.343]   # p-type (Na-doped)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=temp_x, y=zT_n_data, mode="lines+markers",
    name="PbTe n-type (I-doped)",
    line=dict(color="#1e88e5", width=3),
    marker=dict(size=7),
))
fig.add_trace(go.Scatter(
    x=temp_x, y=zT_p_data, mode="lines+markers",
    name="PbTe p-type (Na-doped)",
    line=dict(color="#e53935", width=3),
    marker=dict(size=7),
))
fig.add_hline(y=1.0, line_dash="dot", line_color="grey",
    annotation_text="zT = 1 (practical threshold)", annotation_position="top left")
fig.update_layout(
    xaxis_title="Temperature (K)",
    yaxis_title="Figure of Merit (zT)",
    height=420,
    plot_bgcolor="rgba(240,240,255,0.5)",
    legend=dict(x=0.02, y=0.98),
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Computed from temperature-dependent PbTe transport properties. "
           "Both n- and p-type legs exceed zT > 1 across the 500–800 K working range, "
           "confirming PbTe as an effective mid-temperature thermoelectric material.")

st.subheader("References")
st.markdown("""
1. Materials Project (2025). *PbTe (mp-19717) Structure and Properties*.
2. Sharma, P. K., et al. (2021). *Revisiting thermoelectric properties of PbTe*.
3. Ravich, Y. I., et al. (1970). *Semiconducting lead chalcogenides*.
""")

st.divider()

# --- FOOTER ---
f_col1, f_col2, f_col3 = st.columns([1, 4, 1])

with f_col1:
    try:
        st.image(os.path.join(PROJECT_IMG_DIR, "Program_logo.png"), width=120)
    except:
        pass
with f_col3:
    try:
        st.image(os.path.join(PROJECT_IMG_DIR, "Team_logo.png"), width=120)
    except:
        pass
with f_col2:
    st.markdown("<div style='text-align: center; color: grey;'>© 2026 Adaptive Power Textiles. | Powered by Streamlit.</div>", unsafe_allow_html=True)