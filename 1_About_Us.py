import streamlit as st
import base64
import os

# --- Page Configuration ---
st.set_page_config(page_title="About Us - APT", page_icon="👥", layout="wide")
from theme import apply_global_background

# --- PATH HELPER ---
def _img_path(*parts):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)

apply_global_background(os.path.join("PROJECT IMG", "Hero_background.png"), height_px=1200)

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

# --- HELPER: CONVERT LOCAL IMAGE TO BASE64 FOR HTML ---
def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    except Exception:
        return "https://via.placeholder.com/150?text=Image+Not+Found"

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, li {
        font-family: 'Poppins', sans-serif;
        color: #333;
    }
    
    [data-testid="stSidebar"] {
        top: 100px !important;
        height: calc(100vh - 100px) !important;
    }
    
    [data-testid="collapsedControl"] {
        top: 100px !important;
    }
    
    .section-title {
        font-size: 2rem;
        color: #333;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .team-card {
        padding: 20px;
        text-align: center;
        border-radius: 8px;
        transition: transform 0.2s; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        height: 100%;
    }

    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .team-img {
        width: 120px; 
        height: 120px; 
        border-radius: 50%; 
        object-fit: cover;
        object-position: top;
        margin-bottom: 15px; 
    }
    
    .team-name {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }

    .team-role { 
        font-weight: 400; 
        font-size: 0.9rem; 
        color: #000000;
        margin-bottom: 10px; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }

    .text-block {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #444;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Text ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
st.title("Rethinking Power for Wearables")
st.markdown("""
<div class="text-block">
We are a multidisciplinary team with talented and motivated researchers. 
We focus on making a difference for the industry by harnessing the untapped potential of body heat 
to power the next generation of smart textiles.
<br><br>
No batteries. No wires. Just pure physics woven into fabric.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- The Team ---
st.markdown('<div class="section-title">The Team</div>', unsafe_allow_html=True)

def create_card(name, role, img_path, dark_mode=False):
    img_src = get_img_as_base64(img_path)

    if dark_mode:
        bg_color = "#000000"
        text_color = "#ffffff"
        border = "1px solid #333"
    else:
        bg_color = "#ffffff"
        text_color = "#222222"
        border = "1px solid #f0f2f6"

    return f"""
    <div class="team-card" style="background-color: {bg_color}; border: {border};">
        <img src="{img_src}" class="team-img" style="border: 3px solid {bg_color};">
        <div class="team-name" style="color: {text_color};">{name}</div>
        <div class="team-role">{role}</div>
    </div>
    """

# --- ROW 1 ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown(create_card(
        name="Femi",
        role="Website Developer",
        img_path="PROJECT IMG/Femi.jpg",
        dark_mode=False
    ), unsafe_allow_html=True)

with row1_col2:
    st.markdown(create_card(
        name="Efflam",
        role="Website Developer",
        img_path="PROJECT IMG/Efflam.jpg",
        dark_mode=False
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW 2 ---
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown(create_card(
        name="Akash",
        role="Project Supervisor",
        img_path="PROJECT IMG/Akash.jpg",
        dark_mode=False
    ), unsafe_allow_html=True)

with row2_col2:
    st.markdown(create_card(
        name="UG",
        role="Project Supervisor",
        img_path="PROJECT IMG/UG.jpg",
        dark_mode=False
    ), unsafe_allow_html=True)

with row2_col3:
    st.markdown(create_card(
        name="Alloush",
        role="Project Manager",
        img_path="PROJECT IMG/Alloush.jpg",
        dark_mode=False
    ), unsafe_allow_html=True)

st.markdown("---")

# --- History ---
st.markdown('<div class="section-title">The Project History</div>', unsafe_allow_html=True)
hist_col1, hist_col2 = st.columns([2, 1])

with hist_col1:
    st.markdown("""
The Adaptive Power Textiles project is a research initiative established in 2026. 
It began as a collaborative effort between the **Functional Advanced Materials Engineering With Artificial Intelligence for Sustainability (FAMEAIS) program at Technische Universität Darmstadt** and colleagues at the **Grenoble Materials Science Institute (Grenoble INP)**.
<br><br>
<b>The Pivot</b><br>
Our research direction centers on <b>Thermoelectric Generation (TEG)</b>, 
using Lead Telluride (PbTe) to convert continuous body heat into usable electrical power.
""", unsafe_allow_html=True)

with hist_col2:
    st.info("📍 **Location**")
    st.write("**University Innovation Hub**\n\nAdvanced Materials Lab 4B")
    st.write("📧 contact@apt-project.org")

st.markdown("---")

# --- FOOTER ---
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