# -*- coding: utf-8 -*-

import streamlit as st
import os

def inject_custom_css():
    """Charge la feuille de style externe et l'injecte dans Streamlit."""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css_path = os.path.join(parent_dir, "assets", "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback silencieux ou log simple si le fichier n'est pas trouvé
        pass
