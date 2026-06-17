import streamlit as st
import streamlit.components.v1 as components
import os

parent_dir = os.path.dirname(os.path.abspath(__file__))
component_dir = os.path.join(parent_dir, "my_component")
timing_slider = components.declare_component("timing_slider", path=component_dir)

st.title("Test Component Isolation")
res = timing_slider(action="attack", key="test_key", height=185)
st.write(f"Result is: {res}")
