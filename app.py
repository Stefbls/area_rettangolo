import streamlit as st

st.set_page_config(page_title="Calcolo area rettangolo", page_icon="📐")

st.title("📐 Calcolo dell'area di un rettangolo")
st.write("Inserisci base e altezza in centimetri per calcolare l'area.")

# Input
b = st.number_input("Base b (cm)", min_value=0.0, step=0.1)
h = st.number_input("Altezza h (cm)", min_value=0.0, step=0.1)

# Calcolo
if st.button("Calcola area"):
    area = b * h
    st.success(f"L'area del rettangolo è **{area:.2f} cm²**")
