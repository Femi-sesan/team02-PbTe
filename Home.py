import sys, os
# ── Prevent any local numpy.py from shadowing the installed package ──────────
_cwd = os.path.dirname(os.path.abspath(__file__))
if _cwd in sys.path:
    sys.path.remove(_cwd)
    sys.path.append(_cwd)   # move it to the END so installed packages win
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Home - Adaptive Power Textiles",
    page_icon="⚡",
    layout="wide",
)

# --- HELPER: LOAD BACKGROUND IMAGE ---
def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for CSS."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
hero_img_path = os.path.join(current_dir, "PROJECT IMG", "Hero_background.png")
hero_b64 = get_img_as_base64(hero_img_path) if os.path.exists(hero_img_path) else ""


# --- 3D WEARABLE CONCEPT MODEL ---
def create_wearable_model():
    fig = go.Figure()

    z = np.linspace(0, 10, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = 3 * np.cos(theta_grid)
    y_grid = 2 * np.sin(theta_grid)

    fig.add_trace(go.Surface(
        z=z_grid, x=x_grid, y=y_grid,
        colorscale='Greys', showscale=False, opacity=0.3,
        name="Smart Textile Base"
    ))

    patch_z = [7, 7, 5, 5, 3, 3]
    patch_theta = [0, np.pi, 0.5, np.pi+0.5, -0.5, np.pi-0.5]

    px, py, pz = [], [], []
    for t, h in zip(patch_theta, patch_z):
        px.append(3.1 * np.cos(t))
        py.append(2.1 * np.sin(t))
        pz.append(h)

    fig.add_trace(go.Scatter3d(
        x=px, y=py, z=pz,
        mode='markers',
        marker=dict(
            size=15,
            color='#007BFF',
            symbol='square',
            line=dict(color='white', width=2),
            opacity=0.9
        ),
        name="Integrated TEG Modules"
    ))

    fig.add_trace(go.Scatter3d(
        x=px, y=py, z=pz,
        mode='lines',
        line=dict(color='#B87333', width=4),
        name="Conductive Yarns"
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.6, y=1.6, z=0.6)),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=250,
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
                top: 0; left: 0;
                width: 100%;
                z-index: 999999;
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 1.5rem 3rem;
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
            st.image("PROJECT IMG/Program_logo.png", width=85)
        except:
            st.write("⚡ FAME AIS")
        try:
            st.image("PROJECT IMG/Team_logo.png", width=85)
        except:
            st.write("⚡ PbTe Ligence")

    with col_nav:
        nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(6)
        with nav1: st.page_link("Home.py", label="Home", icon="🏠")
        with nav2: st.page_link("pages/1_About_Us.py", label="About", icon="👥")
        with nav3: st.page_link("pages/2_The_Science.py", label="Science", icon="⚛️")
        with nav4: st.page_link("pages/3_The_Technology.py", label="Tech", icon="🔬")
        with nav5: st.page_link("pages/4_Analytical_Analysis.py", label="Analysis", icon="📈")
        with nav6: st.page_link("pages/5_COMSOL_Simulation.py", label="COMSOL", icon="🖥️")

render_header()


# --- CSS STYLING ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, .stApp, p, h1, h2, h3, h4, h5, h6, li {{
    font-family: 'Poppins', sans-serif;
    color: #333;
}}

[data-testid="stSidebar"] {{
    top: 100px !important;
    height: calc(100vh - 100px) !important;
}}
[data-testid="collapsedControl"] {{
    top: 100px !important;
}}

.stApp {{
    background-image: linear-gradient(to bottom,
        rgba(255,255,255,0.6) 0%,
        rgba(255,255,255,0.85) 60%,
        rgba(255,255,255,1.0) 100%
    ), url("data:image/png;base64,{hero_b64}");
    background-position: 0px 0px;
    background-size: 100% 1200px;
    background-repeat: no-repeat;
    background-attachment: scroll;
}}

.hero-container {{
    background-color: transparent;
    padding: 40px;
    margin-bottom: 10px;
    margin-top: 20px;
}}
.hero-title {{
    font-size: 3.5rem;
    font-weight: 700;
    color: #000000;
    line-height: 1.2;
    margin-bottom: 15px;
    text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
}}
.hero-subtitle {{
    font-size: 1.3rem;
    color: #555;
    font-weight: 400;
    margin-bottom: 1.5rem;
}}
.hero-text {{
    font-size: 1.1rem;
    color: #000000;
    font-weight: 500;
    line-height: 1.6;
    max-width: 900px;
}}

.hero-btn-wrap {{
    margin-top: 18px;
}}

.te-hook-container {{
    background-color: rgba(248, 249, 250, 0.9);
    color: #333;
    padding: 25px;
    border-radius: 12px;
    text-align: left;
    border-left: 6px solid #000000;
    border: 1px solid #ddd;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}}
.te-hook-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: #000000;
}}
.te-hook-text {{
    font-size: 0.95rem;
    color: #555;
    margin-bottom: 0px;
    font-weight: 300;
    line-height: 1.5;
}}

.te-btn-gap {{
    height: 16px;
}}

/* ✅ Slim button look (applies only to wrappers we mark as slim-btn) */
.slim-btn div[data-testid="stButton"] > button {{
    padding: 0.45rem 0.95rem !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
}}

/* ✅ Compact success confirmation (no big green bar) */
.notice-success {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid #d9ead3;
    background: rgba(223, 240, 216, 0.65);
    color: #1b5e20;
    font-weight: 600;
}}

.feature-card {{
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #eee;
    height: 100%;
    min-height: 340px;
    transition: transform 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}}
.feature-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}}

h3 {{ color: #000000; }}

.metric-box {{
    text-align: center;
    padding: 15px;
    background-color: white;
    border-radius: 8px;
    border: 1px solid #f0f2f6;
}}
.metric-label {{ font-size: 1rem; color: #666; margin-bottom: 5px; }}
.metric-value {{ font-size: 1.5rem; font-weight: 600; color: #000000; }}
</style>
""", unsafe_allow_html=True)


# --- HERO SECTION ---
with st.container():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Adaptive Power Textiles</h1>
        <p class="hero-subtitle">Engineering High-Performance PbTe for the Next Generation of Wearables.</p>
        <div class="hero-text">
            We are bridging the gap between <b>space-grade efficiency</b> and <b>textile flexibility</b>.
            Our project integrates Lead Telluride (PbTe), proven in NASA's deep space probes into intelligent fabrics capable of
            <b>powering mobile devices</b> using harvested waste heat.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Slim centered hero button (already correct)
    st.markdown('<div class="hero-btn-wrap"></div>', unsafe_allow_html=True)
    hb1, hb2, hb3 = st.columns([2.2, 1.6, 2.2])
    with hb2:
        st.markdown('<div class="slim-btn">', unsafe_allow_html=True)
        if st.button("Explore Analysis →", type="secondary", use_container_width=True):
            st.switch_page("pages/4_Analytical_Analysis.py")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")


# --- THERMOELECTRIC HOOK & 3D MODEL SECTION ---
hook_col1, hook_col2 = st.columns([1, 1], gap="medium")

with hook_col1:
    st.markdown("""
    <div class="te-hook-container">
        <div class="te-hook-title">What are Thermoelectric Materials?</div>
        <div class="te-hook-text">
            <b>Thermoelectric materials facilitate the direct solid-state conversion of thermal energy into electrical power.
            By leveraging the Seebeck effect, they generate electricity from waste heat without moving parts or emissions.
            <br><br>
            Our design integrates these materials directly into the yarn structure, creating a seamless power-generating fabric.</b>
        </div>
        <div class="te-btn-gap"></div>
    """, unsafe_allow_html=True)

    # ✅ Make Learn Science centered + slim like Explore Analysis
    lb1, lb2, lb3 = st.columns([2.2, 1.6, 2.2])
    with lb2:
        st.markdown('<div class="slim-btn">', unsafe_allow_html=True)
        if st.button("Learn Science →", type="secondary", use_container_width=True):
            st.switch_page("pages/2_The_Science.py")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with hook_col2:
    st.plotly_chart(
        create_wearable_model(),
        use_container_width=True,
        config={'displayModeBar': False, 'scrollZoom': False}
    )

    st.markdown("""
    <div style="font-size: 0.75rem; color: #666; text-align: center; margin-top: -10px;">
        <span style='color: #000000;'>■</span> Integrated PbTe Modules &nbsp;
        <span style='color: #B87333;'>▬</span> Conductive Yarns
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")


# --- The Challenge & Solution ---
st.header("The Engineering Challenge")
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("###  The Problem")
    st.warning("""
    **The Material Trade-Off:**
    High-performance inorganic materials (like PbTe) are efficient but brittle. Flexible organic polymers are durable but inefficient.

    **The Static Failure:**
    Standard TEGs are designed for constant temperature gradients. The real world is dynamic—sun, wind, and body movement constantly change the energy landscape.
    """)

with c2:
    st.markdown("###  Our Solution")
    st.success("""
    **Material Core:**
    We use **Lead Telluride (PbTe)**, optimizing it via nanostructuring to lower thermal conductivity while maintaining high electrical performance ($zT > 1.5$).

    **The Charging Application:**
    Our textile design acts as a wearable charging station, capable of topping up **mobile phones and health sensors** purely from environmental heat differences (See *Analysis* page).
    """)

st.markdown("---")


# --- How It Works ---
st.header("System Architecture")
st.write("The fabric acts as a thermal management engine, woven from three specialized yarn types:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3> Thermoelectric Yarns</h3>
        <p><strong>The Generator</strong></p>
        <p>PbTe-based core filaments that convert the temperature delta (ΔT) directly into electricity using the Seebeck effect.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3> Photothermal Yarns</h3>
        <p><strong>The Heater</strong></p>
        <p>Photothermal yarns woven into the outer layer. They efficiently absorb solar radiation to create a "hot side" during the day.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3> Radiative Cooling Yarns</h3>
        <p><strong>The Cooler</strong></p>
        <p>Radiative Cooling yarns that emit heat through the atmospheric window, passively cooling below ambient temp to create a "cold side."</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# --- Roadmap ---
st.header("Project Roadmap")
r_col1, r_col2 = st.columns([2, 1])

with r_col1:
    st.write("Our data-driven approach moves from theoretical modeling to physical prototyping.")
    st.markdown("""
    *   **Phase 1: System Modeling** - Analyzing thermal resistance and electrical outputs using Python.
    *   **Phase 2: Material Optimization** - Selecting the optimal doping concentration for PbTe to maximize $zT$ at 300K-400K.
    *   **Phase 3: Textile Integration** - Weaving simulation and circuit design for the adaptive controller.
    """)

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Target Power Density</div>
            <div class="metric-value">10 mW/cm²</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Target ZT</div>
            <div class="metric-value">> 1.5</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Material</div>
            <div class="metric-value">PbTe</div>
        </div>
        """, unsafe_allow_html=True)

with r_col2:
    try:
        st.image("PROJECT IMG/roadmap_image.png", caption="Development Timeline", use_container_width=True)
    except:
        st.info("Image not found: PROJECT IMG/roadmap_image.png")

st.markdown("---")


# --- Contact (GOOGLE SHEET CONNECTED) ---
st.markdown("###  Connect with the Research Team")
st.write("Interested in the specifications or collaboration? Reach out to us.")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby1j_TFnTshK6S-28gOIFENfKT9uwuBZePfbPU5k0JciXYYPvbCMET9EJVhYQ4h6z5T/exec"

with st.expander("Contact Form"):
    with st.form("contact_form"):
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            name = st.text_input("Name")
        with c_col2:
            email = st.text_input("Email")

        message = st.text_area("Message", height=140)
        submit = st.form_submit_button("Send Inquiry")

    if submit:
        if not name.strip() or not email.strip() or not message.strip():
            st.warning("Please fill in Name, Email, and Message before sending.")
        else:
            payload = {
                "name": name.strip(),
                "email": email.strip(),
                "message": message.strip(),
                "source": "Adaptive Power Textiles - Home"
            }

            with st.spinner("Sending your message..."):
                r = None
                try:
                    # Send JSON (preferred)
                    r = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=20)

                    # Fallback: form-encoded
                    if r.status_code != 200:
                        r = requests.post(GOOGLE_SCRIPT_URL, data=payload, timeout=20)


                except Exception as e:
                    st.error(f"Connection error: {e}")

            # ✅ Success / Fail handling
            if r is not None and r.status_code == 200:
                try:
                    resp = r.json()
                    if resp.get("ok") is True:
                        st.success("✅ Thank you! Your message has been sent to our team.")
                        st.caption("We’ll get back to you as soon as possible.")
                    else:
                        st.error(f"Script responded but did not save. Error: {resp.get('error', 'Unknown')}")
                except Exception:
                    # If script returns plain text like "OK"
                    st.success("✅ Thank you! Your message has been sent to our team.")
                    st.caption("We’ll get back to you as soon as possible.")
            else:
                st.error("❌ Message not sent. Please try again.")

# --- FOOTER ---
f_col1, f_col2, f_col3 = st.columns([1, 4, 1])
with f_col1:
    try:
        st.image("PROJECT IMG/Program_logo.png", width=120)
    except:
        pass
with f_col3:
    try:
        st.image("PROJECT IMG/Team_logo.png", width=60)
    except:
        pass
with f_col2:
    st.markdown(
        "<div style='text-align: center; color: grey;'>© 2026 Adaptive Power Textiles. | Powered by Streamlit.</div>",
        unsafe_allow_html=True
    )