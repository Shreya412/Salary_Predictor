import streamlit as stp
from pred import show_pred
from explore import show_explore

page = stp.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))

if page == "Predict":
    show_pred()
else: 
    show_explore()