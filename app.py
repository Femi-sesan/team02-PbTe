import streamlit as st
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="Home - Adaptive Power Textiles",
    page_icon="⚡",
    layout="wide",
)

# --- Inject Custom CSS (Unified Theme) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"], .main {
        font-family: 'Poppins', sans-serif;
        color: #333;
    }

    /* Navigation Styling */
    .nav-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding-bottom: 20px;
    }
    
    .nav-item {
        margin-left: 25px;
        font-size: 18px;
        font-weight: 600;
        text-decoration: none;
        color: #555;
        transition: color 0.3s;
    }
    
    .nav-item:hover {
        color: #007BFF;
    }
    
    .active-link {
        color: #007BFF !important;
        border-bottom: 2px solid #007BFF;
    }

    /* Hero Section Text */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #007BFF;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #666;
        font-weight: 300;
        margin-bottom: 2rem;
    }

    /* Section Headers */
    h2 {
        color: #333;
        border-left: 5px solid #007BFF;
        padding-left: 15px;
        margin-top: 30px;
    }
    
    h3 {
        color: #007BFF;
        font-weight: 600;
    }

    /* Card Styling for Features */
    .feature-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    /* Call to Action Button Styling (simulated) */
    .cta-button {
        display: inline-block;
        background-color: #007BFF;
        color: white;
        padding: 10px 25px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar ---
col1, col2 = st.columns([1, 3])
with col1:
    # Placeholder for Logo - You can use st.image("PROJECT IMG/logo.png") here
    st.markdown("### ⚡ APT Project") 
with col2:
    st.markdown("""
    <div class="nav-container">
        <a href="#" class="nav-item active-link">Home</a>
        <a href="#" class="nav-item">The Technology</a>
        <a href="#" class="nav-item">Our Research</a>
        <a href="#" class="nav-item">About Us</a>
        <a href="#" class="nav-item">Contact</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Hero Section ---
hero_col1, hero_col2 = st.columns([1, 1], gap="large")

with hero_col1:
    st.markdown('<div style="padding-top: 20px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Adaptive Power Textiles</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Engineering High-Performance PbTe for the Next Generation of Wearables.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    We are bridging the gap between **space-grade efficiency** and **textile flexibility**. 
    Our project integrates Lead Telluride (PbTe)—a material proven in NASA's deep space probes—into intelligent fabrics that harvest energy from body heat, sunlight, and the cold of space.
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Streamlit native button to switch pages (requires Streamlit > 1.30)
    if st.button("Explore the Technology →", type="primary"):
        st.switch_page("pages/1_The_Technology.py") 

with hero_col2:
    # Ideally use a transparent PNG or a clean photo of the textile concept
    st.image("PROJECT IMG/hero_image.png",  use_container_width=True, caption="The future of autonomous energy is woven.")

st.markdown("---")

# --- The Challenge & Solution ---
st.header("The Engineering Challenge")

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("### 🛑 The Problem")
    st.warning("""
    **1. The Material Trade-Off:**
    High-performance inorganic materials (like PbTe) are efficient but brittle. Flexible organic polymers are durable but inefficient.
    
    **2. The Static Failure:**
    Standard TEGs are designed for constant temperature gradients. The real world is dynamic—sun, wind, and body movement constantly change the energy landscape.
    """)

with c2:
    st.markdown("### ✅ Our Solution")
    st.success("""
    **1. Material Core:**
    We utilize **Lead Telluride (PbTe)**, optimizing it via nanostructuring to lower thermal conductivity while maintaining high electrical performance ($zT > 1.5$).
    
    **2. Adaptive Architecture:**
    We don't just rely on body heat. Our textile integrates **Photothermal** and **Radiative Cooling** yarns to actively manage thermal gradients day and night.
    """)

st.markdown("---")

# --- How It Works (Cards Layout) ---
st.header("System Architecture")
st.write("The fabric acts as a thermal management engine, woven from three specialized yarn types:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>⚡ TE Yarns</h3>
        <p><strong>The Generator</strong></p>
        <p>PbTe-based core filaments that convert the temperature delta (ΔT) directly into electricity using the Seebeck effect.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>☀️ PT Yarns</h3>
        <p><strong>The Heater</strong></p>
        <p>Photothermal yarns woven into the outer layer. They efficiently absorb solar radiation to create a "hot side" during the day.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>❄️ RC Yarns</h3>
        <p><strong>The Cooler</strong></p>
        <p>Radiative Cooling yarns that emit heat through the atmospheric window, passively cooling below ambient temp to create a "cold side."</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Roadmap Section ---
st.header("Project Roadmap")
r_col1, r_col2 = st.columns([2, 1])

with r_col1:
    st.write("Our data-driven approach moves from theoretical modeling to physical prototyping.")
    st.markdown("""
    1.  **Phase 1: System Modeling** - Analyzing thermal resistance and electrical outputs using Python & MATLAB.
    2.  **Phase 2: Material Optimization** - Selecting the optimal doping concentration for PbTe to maximize $zT$ at 300K-400K.
    3.  **Phase 3: Textile Integration** - Weaving simulation and circuit design for the adaptive controller.
    """)
    
    # Metric display
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Target Power Density", value="10 mW/cm²")
    m2.metric(label="Target ZT", value="> 1.5")
    m3.metric(label="Material", value="PbTe")

with r_col2:
    st.image("PROJECT IMG/roadmap_image.png", caption="Development Timeline", use_column_width=True)

st.markdown("---")

# --- Contact / Footer ---
st.markdown("### 📩 Connect with the Research Team")
st.write("Interested in the specifications or collaboration? Reach out to us.")

with st.expander("Contact Form"):
    with st.form("contact_form"):
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            name = st.text_input("Name")
        with c_col2:
            email = st.text_input("Email")
        
        message = st.text_area("Message")
        submit = st.form_submit_button("Send Inquiry")
        
        if submit:
            st.success("Thank you for your interest in Adaptive Power Textiles.")

st.markdown("---")
st.caption("© 2025 Adaptive Power Textiles. Powered by Streamlit. | Data Sources: Wiley Thermoelectrics & npj Computational Materials.")
