import os
import glob

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(page_title="Performance Analysis", page_icon="📈", layout="wide")

from theme import apply_global_background

# --- PATH HELPER ---
def _img_path(*parts):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)

apply_global_background(os.path.join("PROJECT IMG", "Hero_background.png"), height_px=1200)

# =========================================================
# UNIVERSAL HEADER
# =========================================================
def render_header():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { display: none; }
            .block-container { padding-top: 150px !important; padding-bottom: 2rem; }

            div[data-testid="stHorizontalBlock"]:has(#fixed-header-marker) {
                position: fixed; top: 0; left: 0; width: 100%;
                z-index: 999999; background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding-top: 1.5rem; padding-bottom: 1.5rem;
                padding-left: 3rem; padding-right: 3rem;
                height: auto; min-height: 100px; align-items: center;
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
        except Exception:
            st.write("⚡ FAME AIS")
        try:
            st.image(_img_path("PROJECT IMG", "Team_logo.png"), width=85)
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

# =========================================================
# CSS
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, li { font-family: 'Poppins', sans-serif; }

    [data-testid="stSidebar"] { top: 100px !important; height: calc(100vh - 100px) !important; }
    [data-testid="collapsedControl"] { top: 100px !important; }

    h1, h2, h3 { color: #000000; }

    .soft-box {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 16px;
        border-radius: 12px;
    }

    .small-muted { color: #777; font-size: 0.85rem; }

    .pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        border: 1px solid #e6e6e6;
        background: #fafafa;
        font-size: 0.85rem;
        color: #333;
        margin-right: 6px;
    }

    .report-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        margin: 14px 0 22px 0;
        background: white;
    }
    .report-table th, .report-table td {
        border: 1px solid #e6e6e6;
        padding: 14px 14px;
        text-align: left;
        vertical-align: middle;
    }
    .report-table th {
        background: #f4f6f8;
        font-weight: 700;
        color: #222;
    }
    .report-table caption {
        caption-side: top;
        text-align: left;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 10px;
        color: #111;
    }
    </style>
""", unsafe_allow_html=True)

def html_table(caption, headers, rows):
    thead = "".join([f"<th>{h}</th>" for h in headers])
    tbody = ""
    for r in rows:
        tds = "".join([f"<td>{cell}</td>" for cell in r])
        tbody += f"<tr>{tds}</tr>"
    return f"""
    <table class="report-table">
        <caption>{caption}</caption>
        <thead><tr>{thead}</tr></thead>
        <tbody>{tbody}</tbody>
    </table>
    """

# =========================================================
# HELPERS
# =========================================================
def calc_resistance(rho, L, A):
    return rho * L / A

def simulate_couple(Sn, Sp, rho_n, rho_p, L, A, dT):
    R_n = calc_resistance(rho_n, L, A)
    R_p = calc_resistance(rho_p, L, A)
    R_int = R_n + R_p
    Voc = (abs(Sn) + abs(Sp)) * dT
    P_max = (Voc**2) / (4 * R_int)
    return P_max, Voc, R_int, R_n, R_p

def show_centered_plot(fig):
    fig.update_xaxes(fixedrange=False)
    fig.update_yaxes(fixedrange=False)
    left, center, right = st.columns([1, 3, 1])
    with center:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "scrollZoom": True,
                "displaylogo": False,
                "responsive": True,
                "modeBarButtonsToAdd": ["zoom2d", "pan2d", "autoScale2d", "resetScale2d"]
            }
        )

def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

VIDEO_ROOT = os.path.join(project_root(), "COMSOL_ASSETS", "video")

def find_video_candidates(*base_names):
    exts = [".mp4", ".mov", ".m4v"]
    candidates = []
    for base in base_names:
        for ext in exts:
            candidates.append(os.path.join(VIDEO_ROOT, f"{base}{ext}"))
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def show_video_card(path, title):
    if not path or not os.path.exists(path):
        st.warning("Video file not found.")
        return False

    st.markdown(f"**{title}**")
    try:
        st.video(path, autoplay=True, muted=True, loop=True)
    except TypeError:
        try:
            st.video(path)
        except Exception:
            st.warning("This video could not be displayed.")
            return False
    return True

# =========================================================
# PAGE INTRO
# =========================================================
st.title("Performance Analysis")

st.markdown("""
This section presents the **analytical calculations** for the thermoelectric generator.

We use:
- a **100 K benchmark case** to understand one-leg and two-leg performance clearly
- a **lower ΔT case** to represent more realistic wearable operation

The analytical results are later compared with the COMSOL simulation results.
""")

# =========================================================
# COMSOL CTA
# =========================================================
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("🖥️ Open COMSOL Simulation Results", use_container_width=True):
        try:
            st.switch_page("pages/5_COMSOL_Simulation.py")
        except Exception:
            st.warning("Navigation failed in this Streamlit version. Use the COMSOL tab in the header.")
            st.page_link("pages/5_COMSOL_Simulation.py", label="🖥️ Go to COMSOL Simulation page →")

st.divider()

# =========================================================
# SIDEBAR INPUTS
# =========================================================
st.sidebar.header("⚙️ Model Inputs")

st.sidebar.subheader("1. Thermal Condition")
delta_T = st.sidebar.slider("Temperature Gradient ΔT [K]", 10, 200, 100)

st.sidebar.subheader("2. Leg Geometry")
L_mm = st.sidebar.number_input("Leg Length L [mm]", value=2.0, step=0.1)
W_mm = st.sidebar.number_input("Leg Width W [mm]", value=1.0, step=0.1)
D_mm = st.sidebar.number_input("Leg Depth D [mm]", value=1.0, step=0.1)

L = L_mm * 1e-3
A = (W_mm * 1e-3) * (D_mm * 1e-3)

st.sidebar.subheader("3. Phone charging estimate")
phone_choice = st.sidebar.selectbox("Phone model used", ["Samsung S25", "iPhone 17", "Google Pixel"], index=0)

default_batt = {
    "Samsung S25": (5000, 3.85),
    "iPhone 17": (3500, 3.85),
    "Google Pixel": (4700, 3.85),
}
default_mAh, default_V = default_batt[phone_choice]

battery_mAh = st.sidebar.number_input("Battery capacity [mAh]", min_value=500, max_value=10000, value=int(default_mAh), step=100)
battery_V = st.sidebar.number_input("Battery nominal voltage [V]", min_value=3.0, max_value=5.0, value=float(default_V), step=0.01)

system_eff = st.sidebar.slider("System efficiency factor (DC-DC + losses)", 0.20, 1.00, 0.70, 0.05)
battery_Wh = (battery_mAh / 1000.0) * battery_V

# =========================================================
# MAIN TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Geometry",
    "Single-Leg (100 K)",
    "Two-Leg Analytical",
    "PbTe Couple",
    "SnSe Benchmark",
    "Application (Charging)",
    "Analytical Summary"
])

# =========================================================
# TAB 1: GEOMETRY
# =========================================================
with tab1:
    st.markdown("""
The project geometry is structured in two levels:

- a **single-leg baseline** used for analytical validation and COMSOL traceability
- a **two-leg thermoelectric couple** used for the device-level architecture

The geometry selection was made to keep the analytical calculations and COMSOL simulations consistent while remaining realistic for textile-integrated thermoelectric design.

The overall logic is simple:

- compact legs help integration into a wearable structure
- the chosen leg length avoids overly short thermal paths
- the cross-section remains manufacturable while keeping electrical resistance within a useful range
""")

    st.divider()

    st.subheader("Single-Leg Geometry")
    st.markdown("""
The single-leg model is the **baseline configuration** used to verify the basic thermoelectric response of PbTe, including open-circuit voltage, internal resistance, and maximum-power transfer behavior.
""")

    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        st.markdown(f"""
        <div class="soft-box">
        <b>Single-leg dimensions</b><br><br>
        Length (L) = {L_mm:.2f} mm<br>
        Width (W) = {W_mm:.2f} mm<br>
        Depth (D) = {D_mm:.2f} mm<br>
        Area = {A:.3e} m²
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="soft-box">
        <b>Why this geometry was retained</b><br><br>
        <b>1 × 1 mm cross-section:</b> practical compromise between compactness and fabrication.<br><br>
        <b>2 mm length:</b> limits high ohmic resistance while avoiding an excessively short thermal path.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        one_leg_geo_video = find_video_candidates("1_leg_geo", "geo_single_leg")
        if one_leg_geo_video:
            show_video_card(one_leg_geo_video, "Single-leg geometry video")

    st.latex(r"R = \frac{L}{\sigma A}")

    st.markdown("""
This geometry promotes predominantly one-dimensional transport along the leg axis, making it suitable for direct comparison between analytical equations and COMSOL outputs.
""")

    st.divider()

    st.subheader("Two-Leg Geometry")
    st.markdown("""
The two-leg thermoelectric couple is the **device-level model** used to represent the actual generator concept more realistically.

It contains:
- one **n-type leg**
- one **p-type leg**
- **copper interconnect plates**
- an **electrically insulating substrate**
""")

    geom_rows = [
        ["P-leg", "PbTe (p-type)", "1 × 1 × 2", "Position: x = 0 mm"],
        ["N-leg", "PbTe (n-type)", "1 × 1 × 2", "Position: x = 1.5 mm"],
        ["Copper bottom plate (P)", "Cu", "1.45 × 1 × 0.002", "Under P-leg"],
        ["Copper bottom plate (N)", "Cu", "1.45 × 1 × 0.002", "Under N-leg"],
        ["Copper top plate", "Cu", "3 × 1 × 0.002", "Electrical interconnect (top)"],
        ["Substrate", "ZnTe / SiC / InAs", "3 × 1 × 0.5", "Electrical insulation + mechanical support"],
    ]

    st.markdown(
        html_table(
            "Geometry & Material Definition (Two-Leg Couple)",
            ["Component", "Material", "Dimensions (mm)", "Notes"],
            geom_rows
        ),
        unsafe_allow_html=True
    )

    st.markdown("""
Compared with the single-leg baseline, this geometry is closer to the real thermoelectric device because it includes both carrier polarities, metallic interconnects, and structural support.
""")

# =========================================================
# TAB 2
# =========================================================
with tab2:
    st.header("One-Leg TEG (Analytical Evaluation at 100 K)")

    st.write(
        "The single-leg PbTe calculation was used as the baseline analytical case before moving to the two-leg device."
    )

    st.subheader("1) Open-circuit voltage of PbTe")
    st.markdown("When a temperature difference is applied across a thermoelectric material, a voltage is generated due to the Seebeck effect.")
    st.latex(r"V_{oc} = S \Delta T")

    st.markdown("""
- V: Open-circuit voltage (V)  
- S: Seebeck coefficient (V/K)  
- ΔT: Temperature difference (K)  
""")

    S_one = -187e-6
    dT_one = 100

    st.markdown("### Parameters Used")
    st.latex(r"S = -187 \times 10^{-6} \; \text{V/K}")
    st.latex(r"\Delta T = 100 \; \text{K}")

    st.markdown("We can notice that:")
    st.latex(r"S < 0")
    st.markdown("""
The negative sign of the Seebeck coefficient indicates the material is **n-type**.
Electrons are the dominant charge carriers; under a temperature gradient, electrons diffuse from hot to cold.
""")

    Voc_one = S_one * dT_one

    st.markdown("### Calculation")
    st.latex(r"V_{oc} = (-187 \times 10^{-6}) \times 100")
    st.latex(r"V_{oc} = -0.0187 \; \text{V}")

    st.markdown(
        f"""
        <div style="text-align:center; margin: 12px 0 18px 0;">
            <span style="
                display:inline-block;
                background:#ffffff;
                border:1px solid #e6e6e6;
                padding:8px 16px;
                border-radius:10px;
                font-weight:800;
                font-size:1.05rem;
                box-shadow:0 2px 6px rgba(0,0,0,0.03);
            ">
                V<sub>oc</sub> = {Voc_one:.4f} V ({Voc_one*1000:.1f} mV)
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("2) Internal resistance of PbTe")
    st.markdown("The internal electrical resistance depends on geometry and electrical conductivity.")
    st.latex(r"R = \frac{L}{\sigma A}")

    L_one = 2e-3
    sigma_one = 6.0976e4
    A_one = 1e-6

    st.markdown("### Parameters Used")
    st.latex(r"L = 2 \times 10^{-3} \; \text{m}")
    st.latex(r"\sigma = 6.0976 \times 10^{4} \; \text{S/m}")
    st.latex(r"A = 1 \times 10^{-6} \; \text{m}^2")

    R_one = L_one / (sigma_one * A_one)

    st.markdown("### Calculation")
    st.latex(r"R = \frac{2 \times 10^{-3}}{(6.0976 \times 10^{4})(1 \times 10^{-6})}")
    st.latex(r"R = 0.0327 \; \Omega")

    components.html(
        f"""
        <div style="
            display:flex; justify-content:center; gap:18px;
            margin:12px 0 18px 0; font-family:Poppins, sans-serif; flex-wrap:wrap;
        ">
            <div style="width:260px; background:#fff; border:1px solid #e6e6e6; border-radius:12px;
                        padding:12px 14px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                <div style="font-weight:800;">R = {R_one:.4f} Ω</div>
                <div style="margin-top:6px; font-weight:700; font-size:0.9rem; color:#2e7d32;">≈ {R_one*1000:.1f} mΩ</div>
            </div>
        </div>
        """,
        height=110,
    )

    st.subheader("3) Current, voltage and power vs load resistance")
    st.markdown("""
The thermoelectric leg is modeled as:
- Ideal voltage source \(V_{oc}\)
- Internal resistance \(R\)
- Load resistance \(R_L\)
""")

    st.latex(r"I(R_L) = \frac{V_{oc}}{R + R_L}")
    st.latex(r"V(R_L) = \frac{V_{oc} R_L}{R + R_L}")
    st.latex(r"P(R_L) = \frac{V_{oc}^2 R_L}{(R + R_L)^2}")

    R_load = np.linspace(0.1 * R_one, 5 * R_one, 200)
    I_curve = -1 * Voc_one / (R_one + R_load)
    V_curve = I_curve * R_load
    P_curve = I_curve**2 * R_load

    P_max_one = (Voc_one**2) / (4 * R_one)
    R_opt_one = R_one

    st.markdown("### Key Results")
    st.markdown(f"Open-circuit voltage:  $V_{{oc}} = {Voc_one:.4f} \\, V$")
    st.markdown(f"Internal resistance:  $R = {R_one:.4f} \\, \\Omega$")
    st.markdown(f"Maximum power:  $P_{{max}} = {P_max_one:.6f} \\, W$")
    st.markdown(f"Optimal load resistance:  $R_L = {R_opt_one:.4f} \\, \\Omega$")

    fig_current = go.Figure()
    fig_current.add_trace(go.Scatter(
        x=R_load * 1000,
        y=I_curve * 1000,
        name="PbTe Current Curve",
        line=dict(color="#2BFF00", width=4)
    ))
    fig_current.update_layout(
        title="Current vs Load Resistance",
        xaxis_title="Load Resistance (mΩ)",
        yaxis_title="Current (mA)",
        height=420
    )
    show_centered_plot(fig_current)

    fig_voltage = go.Figure()
    fig_voltage.add_trace(go.Scatter(
        x=R_load * 1000,
        y=V_curve * 1000,
        name="PbTe Voltage Curve",
        line=dict(color="#FFBB00", width=4)
    ))
    fig_voltage.update_layout(
        title="Voltage vs Load Resistance",
        xaxis_title="Load Resistance (mΩ)",
        yaxis_title="Voltage (mV)",
        height=420
    )
    show_centered_plot(fig_voltage)

    fig_power = go.Figure()
    fig_power.add_trace(go.Scatter(
        x=R_load * 1000,
        y=P_curve * 1000,
        name="PbTe Power Curve",
        line=dict(color="#007BFF", width=4)
    ))
    fig_power.add_trace(go.Scatter(
        x=[R_opt_one * 1000, R_opt_one * 1000],
        y=[0, P_max_one * 1000],
        mode="lines",
        name="Maximum Power Condition (R_L = R)",
        line=dict(color="red", dash="dash")
    ))
    fig_power.update_layout(
        title="Power vs Load Resistance (One-Leg)",
        xaxis_title="Load Resistance (mΩ)",
        yaxis_title="Power (mW)",
        height=420
    )
    show_centered_plot(fig_power)

    st.markdown(
        f"""
        <div class="soft-box">
        <b>Baseline interpretation:</b> the 100 K one-leg calculation establishes the reference PbTe response before moving to the full couple.<br><br>
        <b>Maximum-power condition:</b> R<sub>L</sub> ≈ R<br>
        <b>R<sub>opt</sub>:</b> {R_opt_one:.4f} Ω<br>
        <b>P<sub>max</sub>:</b> {P_max_one*1000:.3f} mW
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# TAB 3
# =========================================================
with tab3:
    st.header("Analytical Derivations (Two-Leg Thermoelectric Couple)")

    st.markdown("""
The analytical model treats a **thermoelectric couple** (n-leg + p-leg) as:
- a Seebeck voltage source generated by the combined Seebeck coefficients  
- a series internal resistance equal to the sum of both leg resistances

The 100 K case is used as the benchmark analytical validation, while smaller ΔT values can be explored to represent realistic wearable operation.
""")

    Sn = -200e-6
    sigma_n = 100000.0

    p_choice_local = st.selectbox(
        "Select p-leg configuration (for derivation tab):",
        ["TAGS-85 (Standard)", "PbTe-Na (Homojunction)"],
        key="p_leg_choice_derivation"
    )

    if p_choice_local == "TAGS-85 (Standard)":
        Sp = 210e-6
        sigma_p = 85000.0
        st.caption("TAGS-85 p-type counterpart (representative mid-temperature values).")
    else:
        Sp = 240e-6
        sigma_p = 90000.0
        st.caption("PbTe-Na p-type counterpart (representative matched-family values).")

    st.subheader("1) Open-circuit voltage (couple)")
    st.latex(r"V_{oc} = (|S_n| + |S_p|)\,\Delta T")
    Voc = (abs(Sn) + abs(Sp)) * delta_T

    st.markdown(
        f"""
        <div style="text-align:center; margin: 12px 0 18px 0;">
            <span style="
                display:inline-block;
                background:#ffffff;
                border:1px solid #e6e6e6;
                padding:8px 16px;
                border-radius:10px;
                font-weight:800;
                font-size:1.05rem;
                box-shadow:0 2px 6px rgba(0,0,0,0.03);
            ">
                V<sub>oc</sub> = {Voc:.6f} V  ({Voc*1000:.2f} mV)
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("2) Internal resistance (couple)")
    st.latex(r"R_{int} = R_n + R_p")
    st.latex(r"R_n = \frac{L}{\sigma_n A}, \quad R_p = \frac{L}{\sigma_p A}")

    Rn = L / (sigma_n * A) if A > 0 else np.nan
    Rp = L / (sigma_p * A) if A > 0 else np.nan
    Rint = Rn + Rp

    components.html(
        f"""
        <div style="
            display:flex; justify-content:center; gap:18px;
            margin:12px 0 18px 0; font-family:Poppins, sans-serif; flex-wrap:wrap;
        ">
            <div style="width:220px; background:#fff; border:1px solid #e6e6e6; border-radius:12px;
                        padding:12px 14px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                <div style="font-weight:800;">Rₙ = {Rn:.6f} Ω</div>
                <div style="margin-top:6px; font-weight:700; font-size:0.9rem; color:#2e7d32;">≈ {Rn*1000:.2f} mΩ</div>
            </div>
            <div style="width:220px; background:#fff; border:1px solid #e6e6e6; border-radius:12px;
                        padding:12px 14px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                <div style="font-weight:800;">Rₚ = {Rp:.6f} Ω</div>
                <div style="margin-top:6px; font-weight:700; font-size:0.9rem; color:#2e7d32;">≈ {Rp*1000:.2f} mΩ</div>
            </div>
            <div style="width:220px; background:#fff; border:1px solid #e6e6e6; border-radius:12px;
                        padding:12px 14px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                <div style="font-weight:800;">R<sub>int</sub> = {Rint:.6f} Ω</div>
                <div style="margin-top:6px; font-weight:700; font-size:0.9rem; color:#2e7d32;">≈ {Rint*1000:.2f} mΩ</div>
            </div>
        </div>
        """,
        height=150,
    )

    st.subheader("3) Power vs load resistance")
    st.latex(r"I(R_L) = \frac{V_{oc}}{R_{int} + R_L}")
    st.latex(r"P(R_L) = \frac{V_{oc}^2 R_L}{(R_{int}+R_L)^2}")

    RL = np.linspace(0.05 * max(Rint, 1e-9), 5 * max(Rint, 1e-9), 250)
    I = Voc / (Rint + RL)
    P = I**2 * RL

    Pmax = (Voc**2) / (4 * Rint) if Rint > 0 else np.nan
    Ropt = Rint

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=RL * 1000, y=P * 1000, mode="lines", name="Power curve"))
    fig.add_trace(go.Scatter(
        x=[Ropt * 1000, Ropt * 1000],
        y=[0, Pmax * 1000],
        mode="lines",
        name="Max power condition (R<sub>L</sub> = R<sub>int</sub>)",
        line=dict(dash="dash")
    ))
    fig.update_layout(
        title="Couple power vs load resistance",
        xaxis_title="Load Resistance (mΩ)",
        yaxis_title="Power (mW)",
        height=420
    )
    show_centered_plot(fig)

    st.markdown(f"""
<div class="soft-box">
<b>Analytical couple result for ΔT = {delta_T} K</b><br><br>
<b>Maximum-power condition:</b> R<sub>L</sub> ≈ R<sub>int</sub><br>
<b>R<sub>opt</sub>:</b> {Ropt:.6f} Ω<br>
<b>P<sub>max</sub>:</b> {Pmax*1000:.4f} mW
</div>
""", unsafe_allow_html=True)

    st.divider()
    st.subheader("ΔT scaling")
    st.latex(r"P \propto (\Delta T)^2")
    st.latex(r"\left(\frac{100}{20}\right)^2 = 25")
    st.markdown("""
Under first-order analytical assumptions, a **100 K** temperature gradient yields approximately **25×** more power than a **20 K** gradient.

This is why 100 K is useful as a benchmark, while lower ΔT values are more realistic for wearable body-heat harvesting.
""")

# =========================================================
# TAB 4
# =========================================================
with tab4:
    st.header("PbTe Couple")

    col_input, col_res = st.columns(2, gap="large")

    with col_input:
        st.subheader("Material selection")

        st.markdown("**N-leg: PbTe (doped I)**")
        Sn_pbte = -200e-6
        sig_n_pbte = 100000.0
        st.caption(f"Seebeck: {Sn_pbte*1e6:.0f} μV/K | Conductivity: {sig_n_pbte:.0f} S/m")

        st.markdown("**P-leg counterpart**")
        p_choice = st.selectbox("Select counterpart:", ["TAGS-85 (Standard)", "PbTe-Na (Homojunction)"], key="p_leg_choice_main")

        if p_choice == "TAGS-85 (Standard)":
            Sp_val = 210e-6
            sig_p_val = 85000.0
            st.caption("TAGS-85: mid-temperature p-type counterpart.")
        else:
            Sp_val = 240e-6
            sig_p_val = 90000.0
            st.caption("PbTe-Na: matched family for improved mechanical compatibility.")

        st.info("""
**Project interpretation**
- **100 K** is the benchmark analytical case.
- Lower ΔT values can be used to represent realistic wearable operation.
- The detailed substrate comparison is presented on the COMSOL page.
""")

    P_pbte, V_pbte, R_pbte, Rn_pbte, Rp_pbte = simulate_couple(
        Sn_pbte, Sp_val,
        1/sig_n_pbte, 1/sig_p_val,
        L, A, delta_T
    )

    with col_res:
        st.subheader("Outputs (single couple)")
        st.metric("Open-circuit voltage Voc", f"{V_pbte*1000:.2f} mV")
        st.metric("Internal resistance Rint", f"{R_pbte*1000:.2f} mΩ")
        st.metric("Maximum power Pmax", f"{P_pbte*1000:.3f} mW")

        st.markdown(
            """
            <div style="color:#666; font-size:0.95rem; margin-top: -6px;">
            <span class="pill">Impedance matching</span>
            Peak power occurs near <b>Rload ≈ Rint</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

    R_load_pbte = np.linspace(0.1 * R_pbte, 5 * R_pbte, 160)
    I_curve_pbte = V_pbte / (R_pbte + R_load_pbte)
    P_curve_pbte = I_curve_pbte**2 * R_load_pbte

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=R_load_pbte * 1000, y=P_curve_pbte * 1000,
        name="PbTe couple",
        line=dict(color="#007BFF", width=4)
    ))
    fig.update_layout(
        title=f"Power vs load resistance (PbTe couple, ΔT = {delta_T} K)",
        xaxis_title="Load Resistance (mΩ)",
        yaxis_title="Power (mW)",
        height=420
    )
    show_centered_plot(fig)

# =========================================================
# TAB 5
# =========================================================
with tab5:
    st.header("SnSe Benchmark")

    st.markdown("""
SnSe is included as a benchmark to contextualize material choice.
The comparison highlights the trade-off between theoretical performance and engineering integration.
""")

    c_snse, c_comp = st.columns(2, gap="large")

    with c_snse:
        st.info("Benchmark values (representative)")
        S_snse = 500e-6
        sig_snse = 15000.0

        P_snse, V_snse, R_snse, _, _ = simulate_couple(
            -S_snse, S_snse,
            1/sig_snse, 1/sig_snse,
            L, A, delta_T
        )

        delta_pct = ((P_snse - P_pbte) / P_pbte) * 100 if P_pbte != 0 else 0.0
        st.metric("SnSe Pmax", f"{P_snse*1000:.3f} mW", delta=f"{delta_pct:.0f}% vs PbTe")

        st.write(f"Seebeck (combined): **{1000} μV/K**")
        st.write(f"Conductivity: **{sig_snse:.0f} S/m**")

    with c_comp:
        st.warning("Engineering constraints")
        st.markdown(f"""
- Brittle microstructure complicates flexible integration.  
- Higher internal resistance (**{R_snse*1000:.1f} mΩ**) can make electrical matching more demanding.  
- Even if SnSe can outperform PbTe in theory, PbTe remains more aligned with the textile-integration objective.
""")

    R_load_snse = np.linspace(0.1 * R_snse, 5 * R_snse, 160)
    P_curve_snse = (V_snse / (R_snse + R_load_snse))**2 * R_load_snse

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=R_load_pbte * 1000, y=P_curve_pbte * 1000, name="PbTe (selected)"))
    fig2.add_trace(go.Scatter(x=R_load_snse * 1000, y=P_curve_snse * 1000, name="SnSe (benchmark)"))
    fig2.update_layout(
        title="PbTe vs SnSe — power vs load resistance",
        xaxis_title="Load Resistance (mΩ)",
        yaxis_title="Power (mW)",
        height=420
    )
    show_centered_plot(fig2)

# =========================================================
# TAB 6
# =========================================================
with tab6:
    st.header("Application (Charging)")

    st.markdown("""
This section estimates whether a PbTe thermoelectric module could provide a useful charging output for a mobile device.
""")

    target_voltage = 5.0
    V_operating = V_pbte / 2 if V_pbte != 0 else 0.0
    couples_needed = int(np.ceil(target_voltage / V_operating)) if V_operating > 0 else 0

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        st.metric("Voltage per couple under load", f"{V_operating*1000:.2f} mV")
    with col_b:
        st.metric("Couples required in series for ~5 V", f"{couples_needed}")

    st.divider()

    module_power_W = P_pbte * couples_needed if couples_needed > 0 else 0.0
    useful_power_W = module_power_W * system_eff if module_power_W > 0 else 0.0
    charge_time_hours = battery_Wh / useful_power_W if useful_power_W > 0 else np.inf

    res1, res2 = st.columns(2, gap="large")
    with res1:
        st.markdown(
            f"""
            <div class="soft-box">
            <b>Module specification</b><br><br>
            Battery energy = {battery_Wh:.2f} Wh<br>
            Total raw module power = {module_power_W:.4f} W<br>
            Effective usable power = {useful_power_W:.4f} W<br>
            System efficiency = {system_eff:.0%}
            </div>
            """,
            unsafe_allow_html=True
        )

    with res2:
        if np.isfinite(charge_time_hours):
            st.markdown(
                f"""
                <div class="soft-box">
                <b>Estimated charging time</b><br><br>
                {charge_time_hours:.1f} hours
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="soft-box">
                <b>Estimated charging time</b><br><br>
                Not available for the current settings.
                </div>
                """,
                unsafe_allow_html=True
            )

    st.caption("This estimate assumes a sustained temperature gradient and idealized module scaling, so real wearable charging performance would usually be lower.")

# =========================================================
# TAB 7
# =========================================================
with tab7:
    st.header("Analytical Summary")

    st.markdown("""
This summary brings together the analytical milestones used in the project before the detailed COMSOL comparison.
""")

    delta_T_100 = 100
    delta_T_20 = 20

    Sn_sum = -200e-6
    Sp_sum = 240e-6
    sig_n_sum = 100000.0
    sig_p_sum = 90000.0

    P_100, V_100, R_100, _, _ = simulate_couple(
        Sn_sum, Sp_sum,
        1/sig_n_sum, 1/sig_p_sum,
        L, A, delta_T_100
    )

    P_20, V_20, R_20, _, _ = simulate_couple(
        Sn_sum, Sp_sum,
        1/sig_n_sum, 1/sig_p_sum,
        L, A, delta_T_20
    )

    analytical_rows = [
        ["One-leg PbTe baseline", "100", f"{Voc_one*1000:.2f}", f"{R_one*1000:.2f}", f"{P_max_one*1000:.3f}"],
        ["Two-leg benchmark couple", "100", f"{V_100*1000:.2f}", f"{R_100*1000:.2f}", f"{P_100*1000:.3f}"],
        ["Lower-gradient wearable case", "20", f"{V_20*1000:.2f}", f"{R_20*1000:.2f}", f"{P_20*1000:.3f}"],
    ]

    st.markdown(
        html_table(
            "Analytical milestones",
            ["Case", "ΔT (K)", "Voc (mV)", "Rint (mΩ)", "Pmax (mW)"],
            analytical_rows
        ),
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div class="soft-box">
        <b>Analytical conclusion:</b><br><br>
        The 100 K cases were used as benchmark calculations to establish the expected PbTe generator behavior under a strong thermal gradient.  
        Lower ΔT cases were then considered as more realistic wearable operating conditions.  
        As expected, reducing the temperature gradient lowers both output voltage and power, but it gives a more realistic picture for body-heat energy harvesting in a flexible thermoelectric jacket.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link("pages/5_COMSOL_Simulation.py", label="🖥️ Go to COMSOL Simulation page →")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns([1, 4, 1])
with f_col1:
    try:
        st.image(_img_path("PROJECT IMG", "Program_logo.png"), width=120)
    except Exception:
        pass
with f_col3:
    try:
        st.image(_img_path("PROJECT IMG", "Team_logo.png"), width=120)
    except Exception:
        pass
with f_col2:
    st.markdown(
        "<div style='text-align: center; color: grey;'>© 2026 Adaptive Power Textiles. | Powered by Streamlit.</div>",
        unsafe_allow_html=True
    )