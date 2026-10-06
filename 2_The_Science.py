import os

import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="Science - APT", page_icon="⚛️", layout="wide")
from theme import apply_global_background

# --- PATH HELPER ---
def _img_path(*parts):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)

apply_global_background(os.path.join("PROJECT IMG", "Hero_background.png"), height_px=1200)
# --- PROFESSIONAL 3D TEG MODEL FUNCTION (UPDATED COLORS) ---
def create_teg_model():
    """Generates a high-fidelity 3D Plotly figure of a PbTe Module."""

    # --- 1. CONFIGURATION & COLORS ---
    N_LEG_COLOR = '#00BFFF'   # Blue (N-Type)
    P_LEG_COLOR = '#FF6347'   # Red (P-Type)
    COPPER_COLOR = '#B87333'
    HOT_PLATE_COLOR = 'rgba(255, 65, 54, 0.3)'
    COLD_PLATE_COLOR = 'rgba(0, 116, 217, 0.3)'

    fig = go.Figure()

    # --- 2. HELPER: CREATE BOX ---
    def make_box(x_c, y_c, z_c, dx, dy, dz, color, name, shine=False):
        x = [x_c-dx/2, x_c+dx/2, x_c+dx/2, x_c-dx/2, x_c-dx/2, x_c+dx/2, x_c+dx/2, x_c-dx/2]
        y = [y_c-dy/2, y_c-dy/2, y_c+dy/2, y_c+dy/2, y_c-dy/2, y_c-dy/2, y_c+dy/2, y_c+dy/2]
        z = [z_c-dz/2, z_c-dz/2, z_c-dz/2, z_c-dz/2, z_c+dz/2, z_c+dz/2, z_c+dz/2, z_c+dz/2]

        lighting = dict(ambient=0.5, diffuse=0.8, specular=0.9, roughness=0.1) if shine else dict()

        return go.Mesh3d(
            x=x, y=y, z=z,
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            color=color,
            name=name,
            flatshading=True,
            hoverinfo='name',
            lighting=lighting,
            lightposition=dict(x=100, y=200, z=150)
        )

    # --- 3. BUILD THE STRUCTURE ---
    fig.add_trace(make_box(0, 0, 2.2, 5.5, 3, 0.2, HOT_PLATE_COLOR, "Hot Substrate (Ceramic)"))
    fig.add_trace(make_box(0, 0, -2.2, 5.5, 3, 0.2, COLD_PLATE_COLOR, "Cold Substrate (Ceramic)"))

    positions = [-1.8, -0.6, 0.6, 1.8]
    for i, pos in enumerate(positions):
        is_p_type = i % 2 != 0
        leg_name = "PbTe P-Type (Holes+)" if is_p_type else "PbTe N-Type (Electrons-)"
        leg_color = P_LEG_COLOR if is_p_type else N_LEG_COLOR

        fig.add_trace(make_box(pos, 0, 0, 0.8, 2, 3.8, leg_color, leg_name, shine=True))

        # Charge carrier markers (visual only)
        particle_color = 'white'
        pz = np.linspace(-1.5, 1.5, 8)
        px = np.random.normal(pos, 0.1, 8)
        py = np.random.normal(0, 0.5, 8)

        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode='markers',
            marker=dict(size=4, color=particle_color, opacity=0.8),
            name="Charge Carriers",
            showlegend=False
        ))

    # Connectors
    fig.add_trace(make_box(-1.2, 0, -2.0, 2.2, 2, 0.2, COPPER_COLOR, "Copper Interconnect", shine=True))
    fig.add_trace(make_box(1.2, 0, -2.0, 2.2, 2, 0.2, COPPER_COLOR, "Copper Interconnect", shine=True))
    fig.add_trace(make_box(0, 0, 2.0, 2.2, 2, 0.2, COPPER_COLOR, "Copper Interconnect", shine=True))
    fig.add_trace(make_box(-2.0, 0, 2.0, 1.0, 2, 0.2, COPPER_COLOR, "Terminal (-)", shine=True))
    fig.add_trace(make_box(2.0, 0, 2.0, 1.0, 2, 0.2, COPPER_COLOR, "Terminal (+)", shine=True))

    # Heat flux arrow
    fig.add_trace(go.Cone(
        x=[3.5], y=[0], z=[1.5],
        u=[0], v=[0], w=[-1],
        sizemode="absolute", sizeref=2,
        anchor="tail",
        colorscale=[[0, 'orange'], [1, 'red']],
        showscale=False,
        name="Heat Flux"
    ))

    # Labels
    fig.add_trace(go.Scatter3d(
        x=[0, 3.5, -2.8], y=[0, 0, 0], z=[2.6, 0.5, 0],
        mode='text',
        text=["HOT SIDE (Heat Source)", "Heat Flux (ΔT)", "PbTe Couples<br>(N-Blue, P-Red)"],
        textfont=dict(size=12, color="black", family="Arial Black"),
        showlegend=False
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2), center=dict(x=0, y=0, z=0)),
            annotations=[
                dict(
                    showarrow=False, x=0, y=0, z=-2.5,
                    text="COLD SIDE (Radiative Cooling)",
                    font=dict(color="blue", size=12, family="Arial Black"),
                    opacity=0.7
                )
            ]
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- UNIVERSAL HEADER FUNCTION ---
def render_header():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { display: none; }
            .block-container {
                padding-top: 150px !important;
                padding-bottom: 2rem;
            }
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
                min-height: 100px;
                align-items: center;
            }
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
            st.image(_img_path("PROJECT IMG", "Program_logo.png"), width=85)
        except:
            st.write("⚡ FAME AIS")
        try:
            st.image(_img_path("PROJECT IMG", "Team_logo.png"), width=85)
        except:
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

# --- CSS Styling for Educational Content ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, li { font-family: 'Poppins', sans-serif; }

    [data-testid="stSidebar"] {
        top: 100px !important;
        height: calc(100vh - 100px) !important;
    }
    [data-testid="collapsedControl"] { top: 100px !important; }

    .science-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 30px;
    }
    .science-sub {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 50px;
    }

    .highlight-box {
        background-color: #f0f7ff;
        border-left: 5px solid #000000;
        padding: 20px;
        border-radius: 5px;
        margin: 20px 0;
    }

    .zt-box {
        background-color: #f1f1f1;
        color: #333;
        padding: 20px 40px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
        width: fit-content;
        margin: 0 auto;
        display: block;
    }

    h2 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 40px; }
    h3 { color: #000000; margin-top: 20px; }

    .text-justify { text-align: justify; }
    </style>
""", unsafe_allow_html=True)

# --- 1. Introduction ---
st.markdown('<div class="science-header">The Science of Thermoelectrics</div>', unsafe_allow_html=True)
st.markdown('<div class="science-sub">Understanding the physics that allows us to power the future with heat.</div>', unsafe_allow_html=True)

col_def1, col_def2 = st.columns([2, 1], gap="large")

with col_def1:
    st.markdown("### What Are Thermoelectric Devices?")
    st.markdown("""
    <div class="text-justify">
    There are a lot of processes that produce heat: car engines, power plants, factories, computers, and even household appliances.
    Most of this heat cannot be captured or reused easily, so it simply escapes into the air. This unusable heat is known as <b>waste heat</b>.

    Now imagine a device that can take this waste heat and turn it into useful energy. Or one that can use a small amount of electricity
    to create cooling, all without moving parts, noise, or harmful chemicals.

    Such devices are called <b>THERMOELECTRIC DEVICES</b>.
    They have a unique ability to directly convert a temperature difference into electric power and vice versa.
    </div>
    """, unsafe_allow_html=True)

with col_def2:
    st.info("**Key Takeaway:**\n\nThey capture energy that would otherwise be lost forever.\n\nFrom industrial pipes to the human body, any temperature difference is a potential power source.")

st.divider()

# --- 2. History ---
st.markdown("### A Short History")
st.write("The journey from a compass needle twitch to powering Mars rovers.")

hist_tab1, hist_tab2, hist_tab3 = st.tabs(["The Discovery (1800s)", "The Semiconductor Era (1950s)", "Modern Nanotech (2000s+)"])

with hist_tab1:
    st.markdown("""
    *   **1821 - Thomas Johann Seebeck:** He noticed that a compass needle would deflect when a closed loop of two different metals was heated at one junction.
    *   **1834 - Jean Charles Athanase Peltier:** Passing an electric current through a junction caused one side to heat and the other to cool.
    """)

with hist_tab2:
    st.markdown("""
    *   **1950s - Abram Ioffe:** Applied semiconductor theory, enabling materials like **Bi2Te3** and **PbTe**.
    *   **Space Race:** NASA used RTGs where solar panels cannot work.
    """)

with hist_tab3:
    st.markdown("""
    *   **Today - Nanostructuring:** Scatter phonons (heat) while keeping electrons moving to improve efficiency.
    *   **Flexible Wearables:** Focus on flexible inorganic films and polymers for body-heat harvesting.
    """)

st.divider()

# --- 3. Working Principle ---
st.markdown("### How Do They Work?")
main_col1, main_col2 = st.columns([1.2, 1], gap="large", vertical_alignment="center")

with main_col1:
    st.markdown("#### The Seebeck Effect (Power Generation)")
    st.write("These devices react to temperature differences.")
    st.markdown("""
    *   When one side is **hot** and the other is **cold**, charge carriers move from hot to cold.
    *   This movement creates a voltage potential, generating **electricity**.
    """)
    st.latex(r"V = S \times \Delta T")

    st.info("""
    **Optimization:** Maximum power is achieved when the external load resistance matches the internal resistance (impedance matching).
    Increasing the temperature difference ($\Delta T$) also improves output.
    """)

with main_col2:
    st.plotly_chart(create_teg_model(), use_container_width=True, config={'displayModeBar': False})
    st.markdown(
        """<div style="font-size: 0.8rem; color: grey; text-align: center; margin-top: -5px;">
        <b>Interactive 3D:</b> n-type and p-type legs allowing charge flow.
        </div>""",
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("#### The Peltier Effect (Cooling)")
st.markdown("""
*   When you send **electricity** through the material, it reverses the effect.
*   One side becomes **hot** and the other becomes **cold**.
*   This enables solid-state cooling without refrigerants or moving parts.
""")
st.caption("This ability to turn heat into electricity, and electricity into heating or cooling, is the thermoelectric effect.")

st.markdown("---")

# --- 4. Efficiency (zT) ---
st.markdown("### Measuring Efficiency: The Figure of Merit ($zT$)")
st.write("To evaluate thermoelectric quality, we use a dimensionless number called $zT$. Higher is better.")

st.markdown('<div class="zt-box">zT = (S² σ T) / κ</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

z1, z2, z3 = st.columns(3, gap="medium")
with z1:
    st.markdown("**$S$ (Seebeck Coefficient)**")
    st.caption("We want this **HIGH** — more voltage from ΔT.")
with z2:
    st.markdown("**$\\sigma$ (Electrical Conductivity)**")
    st.caption("We want this **HIGH** — current flows easily.")
with z3:
    st.markdown("**$\\kappa$ (Thermal Conductivity)**")
    st.caption("We want this **LOW** — maintain the temperature gradient.")

st.divider()

# --- 5. Common Materials ---
st.markdown("### Most Famous Thermoelectric Materials")
st.write("Materials are selected based on operating temperature range.")

mat_col1, mat_col2, mat_col3 = st.columns(3)

with mat_col1:
    st.markdown("#### Low Temp (< 150°C)")
    st.markdown("**Bismuth Telluride ($Bi_2Te_3$)**")
    st.write("Standard for refrigeration and room-temperature TEGs.")

with mat_col2:
    st.markdown("#### Mid Temp (500–800K)")
    st.markdown("**Lead Telluride ($PbTe$)**")
    st.write("**Our Project Material.**")

    with st.expander("Analysis: Pros & Cons"):
        st.markdown("""
        **Advantages:**
        * High efficiency at mid-temp
        * High-temperature stability
        * Historically proven in space power systems

        **Drawbacks:**
        * Contains lead (toxicity / disposal concern)
        * Brittle (mechanical integration challenge)
        * Tellurium is relatively scarce
        """)

with mat_col3:
    st.markdown("#### High Temp (> 900K)")
    st.markdown("**Silicon-Germanium ($SiGe$)**")
    st.write("Used in deep-space RTGs for extreme environments.")

st.divider()

# --- 6. Applications & Market Chart ---
st.markdown("### Applications & Global Usage")

app_col1, app_col2 = st.columns([1, 1])

with app_col1:
    st.markdown("""
    Thermoelectrics are used where reliability matters:
    * **Space power (RTGs)**
    * **Solid-state cooling**
    * **Industrial waste-heat recovery**
    * **Automotive exhaust harvesting**
    * **Wearables and body-heat devices**
    """)

with app_col2:
    try:
        st.image("PROJECT IMG/market_chart.jpg", caption="Global Thermoelectric Generators Market (Source: Roots Analysis)", use_container_width=True)
    except:
        st.warning("⚠️ Upload the chart image to 'PROJECT IMG' and name it 'market_chart.jpg'.")

st.markdown("---")

# --- 7. References ---
st.markdown("### References")
st.markdown("""
<div style="font-size: 0.9rem; color: #555;">
1. Wu et al. (2022). Thermoelectric converter: Strategies from materials to device application. Nano Energy.
2. Sanad et al. (2020). Thermoelectric Energy Harvesters review. Topics in Current Chemistry.
3. Zhang et al. (2021). Flexible thermoelectric materials and devices. Materials Today.
4. Petsagkourakis et al. (2018). Thermoelectric materials and applications. STAM.
5. Sun et al. (2022). Toward energy harvesting from the human body. Materials Today.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- FOOTER ---
f_col1, f_col2, f_col3 = st.columns([1, 4, 1])
with f_col1:
    try:
        st.image(_img_path("PROJECT IMG", "Program_logo.png"), width=120)
    except:
        pass
with f_col3:
    try:
        st.image(_img_path("PROJECT IMG", "Team_logo.png"), width=120)
    except:
        pass
with f_col2:
    st.markdown("<div style='text-align: center; color: grey;'>© 2026 Adaptive Power Textiles. | Powered by Streamlit.</div>", unsafe_allow_html=True)