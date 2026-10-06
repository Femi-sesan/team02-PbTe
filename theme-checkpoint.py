import base64
import os
import streamlit as st

def get_img_as_base64(file_path: str) -> str:
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def apply_global_background(image_rel_path: str, height_px: int = 1200):
    """
    Apply a global background image + soft white fade overlay.
    image_rel_path: path relative to the current file (page script).
    height_px: how tall the background should be before it becomes fully white.
    """

    # Current page directory (works on every page)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Build full path to the background image
    bg_path = os.path.join(current_dir, image_rel_path)

    bg_b64 = get_img_as_base64(bg_path) if os.path.exists(bg_path) else ""

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: linear-gradient(to bottom,
                    rgba(255,255,255,0.6) 0%,
                    rgba(255,255,255,0.85) 60%,
                    rgba(255,255,255,1.0) 100%
                ), url("data:image/png;base64,{bg_b64}");

                background-position: 0px 0px;
                background-size: 100% {height_px}px;
                background-repeat: no-repeat;
                background-attachment: scroll;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )