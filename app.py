import os
import streamlit as st
from supabase import create_client, Client

# ---- CONFIGURAZIONE ----
st.set_page_config(page_title="Login Demo", page_icon="🔐")

# Leggi le chiavi da .streamlit/secrets.toml
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# ---- FUNZIONE LOGIN ----
def login(email, password):
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["user"] = result.user
        st.session_state["session"] = result.session
        st.success("Login effettuato con successo ✅")
        st.rerun()
    except Exception as e:
        st.error("Credenziali non valide o errore di connessione.")

# ---- FUNZIONE LOGOUT ----
def logout():
    st.session_state.clear()
    st.rerun()

# ---- INTERFACCIA ----
st.title("🔐 Accesso all'app")

# Se non loggato → mostra form login
if "user" not in st.session_state:
    st.subheader("Effettua il login per continuare")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(email, password)

    st.info("Non hai un account? Registrati nel tuo progetto Supabase (Auth > Users).")

# Se loggato → mostra contenuto dell'app
else:
    user = st.session_state["user"]
    st.success(f"Benvenuto, {user.email} 👋")

    # --- CONTENUTO DELL'APP ---
    st.header("Calcolo area rettangolo 📐")
    b = st.number_input("Base b (cm)", min_value=0.0, step=0.1)
    h = st.number_input("Altezza h (cm)", min_value=0.0, step=0.1)
    if st.button("Calcola area"):
        area = b * h
        st.success(f"L'area del rettangolo è **{area:.2f} cm²**")

    st.divider()
    if st.button("Logout"):
        logout()
