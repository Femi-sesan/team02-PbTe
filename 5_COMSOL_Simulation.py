import streamlit as st
import os
import glob
import pandas as pd
from PIL import Image

# --- PATH HELPER ---
def _img_path(*parts):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COMSOL Simulation (Single-Leg & Two-Leg)",
    page_icon="🖥️",
    layout="wide",
)

# --- UNIVERSAL HEADER FUNCTION ---
def render_header():
    st.markdown("""
        <style>
            header[data-testid="stHeader"] { display: none; }

            .block-container {
                padding-top: 140px !important;
                padding-bottom: 2rem;
                max-width: 1380px;
            }

            div[data-testid="stHorizontalBlock"]:has(#fixed-header-marker) {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                z-index: 999999;
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding-top: 1.2rem;
                padding-bottom: 1.2rem;
                padding-left: 3rem;
                padding-right: 3rem;
                min-height: 92px;
                align-items: center;
            }

            div[data-testid="stHorizontalBlock"]:has(#fixed-header-marker) img {
                object-fit: contain !important;
                margin-bottom: 0px !important;
                max-height: 42px !important;
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

# --- CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, li, div, span {
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stSidebar"] {
        top: 96px !important;
        height: calc(100vh - 96px) !important;
    }

    [data-testid="collapsedControl"] {
        top: 96px !important;
    }

    h1, h2, h3 {
        color: #000000;
    }

    .small-muted {
        color: #666;
        font-size: 0.9rem;
    }

    .soft-box {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 16px;
        border-radius: 12px;
    }

    .report-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
        margin: 10px 0 18px 0;
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

    .section-kicker {
        color: #666;
        font-size: 0.95rem;
        margin-top: -4px;
    }

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

    .video-card-title {
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 10px;
        color: #222;
        min-height: 56px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# COMSOL ASSET ROOTS
# =========================
def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ASSETS_ROOT = os.path.join(project_root(), "COMSOL_ASSETS")
IMG_ROOT = os.path.join(ASSETS_ROOT, "images")
DATA_ROOT = os.path.join(ASSETS_ROOT, "data")
VID_ROOT = os.path.join(ASSETS_ROOT, "video")

# =========================
# HELPERS
# =========================
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

def list_files(folder, patterns):
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(folder, p)))
    return sorted(files)

def find_first_existing(paths):
    for p in paths:
        if p and os.path.exists(p):
            return p
    return None

def safe_read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        return None

def data_case_dir(case_name):
    return os.path.join(DATA_ROOT, case_name)

def find_case_csv(case_name):
    folder = data_case_dir(case_name)
    if not os.path.isdir(folder):
        return None
    csvs = list_files(folder, ["*.csv"])
    for p in csvs:
        bn = os.path.basename(p).lower()
        if "power" in bn and ("rload" in bn or "load" in bn):
            return p
    return csvs[0] if csvs else None

def find_case_excel(case_name):
    folder = data_case_dir(case_name)
    if not os.path.isdir(folder):
        return None
    xls = list_files(folder, ["*.xlsx", "*.xls"])
    for p in xls:
        if "maximum_power" in os.path.basename(p).lower():
            return p
    return xls[0] if xls else None

def show_download_button(label, path, mime):
    data = safe_read_bytes(path)
    if data is None:
        st.caption(f"Missing file: {path}")
        return
    st.download_button(
        label=label,
        data=data,
        file_name=os.path.basename(path),
        mime=mime,
        use_container_width=True
    )

def find_image_anywhere(filename):
    candidates = [
        os.path.join(IMG_ROOT, filename),
        os.path.join(IMG_ROOT, "substrate", filename),
        os.path.join(IMG_ROOT, "Substrate", filename),
        os.path.join(VID_ROOT, filename),
        os.path.join("PROJECT IMG", filename),
    ]

    for folder in [
        IMG_ROOT,
        os.path.join(IMG_ROOT, "substrate"),
        os.path.join(IMG_ROOT, "Substrate"),
        VID_ROOT,
        "PROJECT IMG",
    ]:
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if f.lower() == filename.lower():
                    candidates.append(os.path.join(folder, f))

    return find_first_existing(candidates)

def find_video_candidates(*base_names):
    exts = [".mp4", ".mov", ".m4v"]
    candidates = []
    for base in base_names:
        for ext in exts:
            candidates.append(os.path.join(VID_ROOT, f"{base}{ext}"))
    return find_first_existing(candidates)

def show_centered_image(path, caption=None, max_w=950, max_h=520):
    if not path or not os.path.exists(path):
        return False

    img = Image.open(path)
    img.thumbnail((max_w, max_h))

    c1, c2, c3 = st.columns([1, 4.3, 1])
    with c2:
        st.image(img, caption=caption, use_container_width=False)
    return True

def show_video_card(path, title):
    if not path or not os.path.exists(path):
        st.warning("Video file not found.")
        return False

    st.markdown(f'<div class="video-card-title">{title}</div>', unsafe_allow_html=True)

    try:
        st.video(path, autoplay=True, muted=True, loop=True)
    except TypeError:
        try:
            st.video(path)
        except Exception:
            st.warning("This video could not be displayed.")
            return False

    return True

def show_substrate_img(title, filename_options):
    found = None
    for fn in filename_options:
        p = find_image_anywhere(fn)
        if p:
            found = p
            break
    if found:
        show_centered_image(found, caption=title, max_w=700, max_h=420)
    else:
        st.caption(f"Missing: {filename_options[0]} (check COMSOL_ASSETS/video/, COMSOL_ASSETS/images/ or PROJECT IMG/)")

# =========================
# MAIN PAGE
# =========================
st.title("COMSOL Simulation (Single-Leg & Two-Leg Thermoelectric Couple)")
st.markdown("""
This section documents:
- a **baseline single-leg** COMSOL simulation
- the **two-leg thermoelectric couple** simulation
- the **substrate comparison study**
- the **20 K wearable case**
- a final conclusion on the numerical validation
""")

main_tab1, main_tab2, main_tab3 = st.tabs([
    "Single-Leg Simulation",
    "Two-Leg Couple Simulation",
    "Conclusion",
])

# =========================================================
# TAB 1: SINGLE-LEG SIMULATION
# =========================================================
with main_tab1:
    st.header("Single-Leg Simulation")

    st.markdown("""
The single-leg COMSOL model is used as the **baseline validation step**. It allows the thermoelectric response
of PbTe to be checked in a simpler model before moving to the complete two-leg device.
""")

    st.subheader("Material Properties")
    st.markdown("""
The PbTe leg was simulated using representative transport parameters consistent with the analytical model.
""")
    st.latex(r"S = -1.87 \times 10^{-4} \ \text{V/K}")
    st.latex(r"\sigma = 6.0976 \times 10^{4} \ \text{S/m}")
    st.latex(r"k = 1.46 \ \text{W/m.k}")

    st.divider()

    st.subheader("Boundary Conditions")
    st.markdown("A fixed temperature difference of 100 K was imposed across the leg and a load sweep was used to evaluate power delivery.")
    st.latex(r"T_c = 573 \ \text{K}")
    st.latex(r"T_h = 673 \ \text{K}")
    st.latex(r"V = 0")
    st.latex(r"P = I^2R_L")

    st.divider()

    st.subheader("Mesh")
    v_mesh1 = find_video_candidates("1_leg_mesh", "mesh_single_leg")
    if v_mesh1:
        show_video_card(v_mesh1, "Single-leg mesh")

    st.divider()

    st.subheader("Temperature and Voltage Gradient")

    col1, col2 = st.columns([1.5, 1.3], gap="medium")
    with col1:
        st.markdown("""
The temperature distribution inside the PbTe leg shows a nearly linear gradient between the hot and cold surfaces.
""")
        st.latex(r"T_{hot}= 673 K")
        st.latex(r"T_{cold}= 573 K")
        st.latex(r"\Delta T= 100 K")
    with col2:
        v_temp1 = find_video_candidates("1_leg_temp")
        if v_temp1:
            show_video_card(v_temp1, "Temperature distribution")

    col1, col2 = st.columns([1.5, 1.3], gap="medium")
    with col1:
        st.markdown("""
The electric potential distribution confirms the generation of thermoelectric voltage due to the Seebeck effect.
""")
        st.latex(r"V_{oc} = -0.0187 V = -18.7 mV")
    with col2:
        v_voc1 = find_video_candidates("1_leg_VOC")
        if v_voc1:
            show_video_card(v_voc1, "Electric potential distribution")

    v_field1 = find_video_candidates("1_leg_field")
    if v_field1:
        show_video_card(v_field1, "Electric field distribution")

    st.divider()

    st.subheader("Internal Resistance Results")
    iv_img = find_first_existing([
        os.path.join("PROJECT IMG", "IV.png"),
        os.path.join(IMG_ROOT, "IV.png"),
    ])
    show_centered_image(iv_img, caption="Current vs Voltage curve obtained from COMSOL simulation", max_w=860, max_h=470)

    st.latex(r"R_{int} = 0.0328 \ \Omega = 32.8 \ \text{m}\Omega")

    st.divider()

    st.subheader("Power Output Under Load")

    current_img = find_first_existing([
        os.path.join("PROJECT IMG", "Current.png"),
        os.path.join(IMG_ROOT, "Current.png"),
    ])
    voltage_img = find_first_existing([
        os.path.join("PROJECT IMG", "Voltage.png"),
        os.path.join(IMG_ROOT, "Voltage.png"),
    ])
    power_img = find_first_existing([
        os.path.join("PROJECT IMG", "P.png"),
        os.path.join(IMG_ROOT, "P.png"),
    ])

    st.markdown("### Current vs Load Resistance")
    show_centered_image(current_img, max_w=920, max_h=470)

    st.markdown("### Voltage vs Load Resistance")
    show_centered_image(voltage_img, max_w=920, max_h=470)

    st.markdown("### Power vs Load Resistance")
    show_centered_image(power_img, max_w=920, max_h=470)

    st.markdown("Maximum power:  $P_{max} = 0.0027 \\, W$")
    st.markdown("Occurs at  $R_L = 0.0327 \\, \\Omega$")

    st.divider()

    st.subheader("Quantitative Comparison")

    data_single = {
        "Parameter": [
            "Open-circuit Voltage (V)",
            "Internal Resistance (Ω)",
            "Optimal Load Resistance (Ω)",
            "Maximum Power (W)"
        ],
        "COMSOL (Numerical)": [-0.0187, 0.0328, 0.0327, 0.0027],
        "Analytical Model": [-0.0187, 0.0327, 0.0327, 0.002673],
    }
    df_single = pd.DataFrame(data_single)
    df_single["Difference (%)"] = (
        (df_single["COMSOL (Numerical)"] - df_single["Analytical Model"]).abs()
        / df_single["Analytical Model"].abs()
    ) * 100
    st.dataframe(df_single, use_container_width=True)

# =========================================================
# TAB 2: TWO-LEG COUPLE SIMULATION
# =========================================================
with main_tab2:
    st.header("Two-Leg Couple Simulation")

    st.markdown("""
This section presents the COMSOL results for the **two-leg thermoelectric couple**, which serves as the main device-level
reference for the project.
""")

    st.subheader("Material Properties")
    st.latex(r"S_p = 2.40 \times 10^{-4} \ \text{V/K}")
    st.latex(r"S_n = -2.00 \times 10^{-4} \ \text{V/K}")

    st.divider()

    st.subheader("Boundary Conditions")
    st.markdown("A 100 K thermal gradient was imposed and the load resistance was swept to determine the optimal operating point.")
    st.latex(r"T_c = 573 \ \text{K}")
    st.latex(r"T_h = 673 \ \text{K}")
    st.latex(r"V = 0")

    st.divider()

    st.subheader("Mesh")
    v_mesh2 = find_video_candidates("2_legs_mesh", "mesh_two_leg")
    if v_mesh2:
        show_video_card(v_mesh2, "Two-leg mesh")

    st.divider()

    st.subheader("Temperature and Voltage Gradient")

    col1, col2 = st.columns([1.5, 1.3], gap="medium")
    with col1:
        st.markdown("""
The temperature distribution inside the PbTe couple shows a nearly linear gradient between the hot and cold surfaces.
""")
        st.latex(r"T_{hot}= 673 K")
        st.latex(r"T_{cold}= 573 K")
        st.latex(r"\Delta T= 100 K")
    with col2:
        v_temp2 = find_video_candidates("2_legs_temp", "results_two_leg")
        if v_temp2:
            show_video_card(v_temp2, "Temperature distribution")

    col1, col2 = st.columns([1.5, 1.3], gap="medium")
    with col1:
        st.markdown("""
The electric potential distribution confirms the expected thermoelectric voltage development across the couple.
""")
        st.latex(r"V_{oc} = -0.044 V = -44.0 mV")
    with col2:
        v_voc2 = find_video_candidates("2_legs_VOC", "results_two_leg")
        if v_voc2:
            show_video_card(v_voc2, "Electric potential distribution")

    v_field2 = find_video_candidates("2_legs_field")
    if v_field2:
        show_video_card(v_field2, "Electric field distribution")

    st.divider()

    st.subheader("Internal Resistance Results")

    iv2_img = find_first_existing([
        os.path.join("PROJECT IMG", "IV 2legs.png"),
        os.path.join("PROJECT IMG", "IV2legs.png"),
        os.path.join(IMG_ROOT, "IV 2legs.png"),
        os.path.join(IMG_ROOT, "IV2legs.png"),
    ])
    show_centered_image(iv2_img, caption="Current vs Voltage curve obtained from COMSOL simulation", max_w=860, max_h=470)

    st.latex(r"R_{int} = 0.043216 \Omega = 43.2 \ \text{m}\Omega")

    st.divider()

    st.subheader("Power Output Under Load")

    current2_img = find_first_existing([
        os.path.join("PROJECT IMG", "Current 2legs.png"),
        os.path.join("PROJECT IMG", "Current2legs.png"),
        os.path.join(IMG_ROOT, "Current 2legs.png"),
        os.path.join(IMG_ROOT, "Current2legs.png"),
    ])
    voltage2_img = find_first_existing([
        os.path.join("PROJECT IMG", "Voltage 2legs.png"),
        os.path.join("PROJECT IMG", "Voltage2legs.png"),
        os.path.join(IMG_ROOT, "Voltage 2legs.png"),
        os.path.join(IMG_ROOT, "Voltage2legs.png"),
    ])
    power2_img = find_first_existing([
        os.path.join("PROJECT IMG", "P 2legs.png"),
        os.path.join("PROJECT IMG", "P2legs.png"),
        os.path.join(IMG_ROOT, "P 2legs.png"),
        os.path.join(IMG_ROOT, "P2legs.png"),
    ])

    st.markdown("### Current vs Load Resistance")
    show_centered_image(current2_img, max_w=920, max_h=470)

    st.markdown("### Voltage vs Load Resistance")
    show_centered_image(voltage2_img, max_w=920, max_h=470)

    st.markdown("### Power vs Load Resistance")
    show_centered_image(power2_img, max_w=920, max_h=470)

    st.markdown("Maximum power:  $P_{max} = 0.0112 \\, W$")
    st.markdown("Occurs at  $R' = 0.0400 \\, \\Omega$")

    st.divider()

    st.subheader("Substrate Sensitivity Study")
    st.markdown("""
The substrate comparison was carried out for **ZnTe**, **SiC**, and **InAs** to determine whether the supporting layer significantly changes the device response.

From the simulation results, all three substrates behaved mainly as **electrical insulators and structural supports**, while the output voltage remained very close across the three cases.
ZnTe gave the closest agreement with the analytical expectation and was therefore selected for the focused wearable study.
""")

    s1, s2, s3 = st.columns(3, gap="medium")
    with s1:
        show_substrate_img(
            "ZnTe substrate result",
            [
                "ZnTe sub.png",
                "ZnTe sub.jpg",
                "ZnTe sub.jpeg",
                "ZnTe sub.webp",
            ]
        )
    with s2:
        show_substrate_img(
            "SiC substrate result",
            [
                "SiC sub.png",
                "SiC sub.jpg",
                "SiC sub.jpeg",
                "SiC sub.webp",
            ]
        )
    with s3:
        show_substrate_img(
            "InAs substrate result",
            [
                "InAs sub.png",
                "InAs sub.jpg",
                "InAs sub.jpeg",
                "InAs sub.webp",
            ]
        )

    st.markdown(
        html_table(
            "Substrate comparison summary",
            ["Substrate", "Observed output voltage", "Interpretation"],
            [
                ["ZnTe", "≈ 44 mV", "Best agreement with analytical result; selected for focused study"],
                ["SiC", "≈ 43 mV", "Very close to ZnTe; mainly acted as insulating support"],
                ["InAs", "≈ 43 mV", "Very close to ZnTe; mainly acted as insulating support"],
            ]
        ),
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("20 K Wearable Case (ZnTe Selected)")
    st.markdown("""
After selecting **ZnTe** as the preferred substrate, the simulation focus moved to the **20 K** case.

This lower temperature difference is more realistic for the final wearable application because the project targets a
**flexible thermoelectric jacket powered by body heat**.
""")

    c20_1, c20_2 = st.columns(2, gap="medium")

    with c20_1:
        img_temp_20k = find_first_existing([
            os.path.join(VID_ROOT, "20k temp gradient.png"),
            os.path.join(VID_ROOT, "20k temp gradient.jpg"),
            os.path.join(VID_ROOT, "20k temp gradient.jpeg"),
            os.path.join(VID_ROOT, "20k temp gradient.webp"),
        ])
        if img_temp_20k:
            show_centered_image(img_temp_20k, caption="20 K temperature gradient", max_w=760, max_h=420)

    with c20_2:
        img_pot_20k = find_first_existing([
            os.path.join(VID_ROOT, "20k electric potential gradient.png"),
            os.path.join(VID_ROOT, "20k electric potential gradient.jpg"),
            os.path.join(VID_ROOT, "20k electric potential gradient.jpeg"),
            os.path.join(VID_ROOT, "20k electric potential gradient.webp"),
        ])
        if img_pot_20k:
            show_centered_image(img_pot_20k, caption="20 K electric potential gradient", max_w=760, max_h=420)

    st.markdown("### Electric Field Distribution at 20 K")
    v_field20 = find_video_candidates("video elec field 20k")
    if v_field20:
        show_video_card(v_field20, "Electric field distribution at 20 K")

    st.markdown(
        html_table(
            "20 K focused result (ZnTe-selected case)",
            ["Case", "Thot (K)", "Tcold (K)", "ΔT (K)", "Voc (mV)", "Rint (mΩ)", "Rload @ Pmax (Ω)", "Pmax (mW)"],
            [
                ["ZnTe selected case", "310", "290", "20", "3.735", "8.2", "0.01", "0.421"],
            ]
        ),
        unsafe_allow_html=True
    )

# =========================================================
# TAB 3: CONCLUSION
# =========================================================
with main_tab3:
    st.header("Conclusion")

    st.markdown("""
The COMSOL study confirms the main analytical trends of the project and supports the final device interpretation.
""")

    st.markdown("""
- The **single-leg PbTe model** successfully reproduced the expected Seebeck voltage, internal resistance, and matched-load power behavior.  
- The **two-leg PbTe couple** also showed strong agreement with the analytical model, confirming that the device behaves as expected under an applied thermal gradient.  
- At **ΔT = 100 K**, the two-leg device produced a voltage close to **44 mV**, matching the benchmark analytical prediction.  
- The substrate comparison using **ZnTe**, **SiC**, and **InAs** showed only small voltage differences, indicating that the substrate mainly serves as a **support and insulating layer** rather than a dominant power-generating factor.  
- **ZnTe** was selected as the preferred substrate because it produced the closest match to the analytical result and the highest output among the tested cases, even though the difference was small.  
- After substrate selection, the study focus moved to the **20 K case** to represent a more realistic temperature gradient for a **flexible wearable thermoelectric jacket**.  
- As expected, reducing the temperature difference from **100 K to 20 K** reduced both voltage and power output substantially, but this lower-gradient case is more representative of practical body-heat harvesting.  
""")

    st.markdown("""
<div class="soft-box">
<b>Overall project conclusion:</b><br><br>
The combined analytical and COMSOL results show that the PbTe thermoelectric couple is a valid generator concept for wearable energy harvesting studies.  
The analytical model provides a reliable benchmark, COMSOL confirms the multiphysics behavior, and the substrate study shows that ZnTe is the most suitable choice among the tested supports.  
Although the realistic 20 K body-heat case produces a lower output than the 100 K benchmark, it still provides the correct practical basis for designing a flexible thermoelectric jacket.
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
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
        unsafe_allow_html=True,
    )