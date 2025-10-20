import streamlit as st
from supabase import create_client, Client
import os

# --- CONFIGURAZIONE SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://<TUO-PROJECT>.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<TUO-API-KEY-ANON>")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- INTERFACCIA DI LOGIN / SIGNUP ---
st.set_page_config(page_title="Demo Login", page_icon="🔐", layout="centered")

# Funzione per verificare se utente è loggato
if "user" not in st.session_state:
    st.session_state["user"] = None

def login(email, password):
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["user"] = result.user
        st.success(f"Benvenuto {email}!")
        st.rerun()
    except Exception as e:
        st.error("Credenziali non valide o utente inesistente.")

def signup(email, password):
    try:
        result = supabase.auth.sign_up({"email": email, "password": password})
        st.success("Registrazione completata! Controlla la tua email per confermare l'account.")
    except Exception as e:
        st.error("Errore durante la registrazione. L'utente potrebbe già esistere.")

def logout():
    supabase.auth.sign_out()
    st.session_state["user"] = None
    st.rerun()

# --- LOGIN PAGE ---
if st.session_state["user"] is None:
    st.title("🔐 Log in")

    login_method = st.radio("Scegli come accedere:", ["Email & Password", "Google"], horizontal=True)

    if login_method == "Email & Password":
        tab_login, tab_signup = st.tabs(["Log in", "Sign up"])

        with tab_login:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Log in"):
                login(email, password)

        with tab_signup:
            email_su = st.text_input("Email (nuovo utente)")
            password_su = st.text_input("Password (nuovo utente)", type="password")
            if st.button("Sign up for free"):
                signup(email_su, password_su)

    elif login_method == "Google":
        st.markdown(
            f"[🔗 Log in with Google]({SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=http://localhost:8501)"
        )
        st.info("Questo link aprirà la finestra di login Google (funziona se hai configurato il provider in Supabase).")

else:
    # --- APP PRINCIPALE ---
    st.title("📏 Calcolo area del rettangolo")
    st.write(f"Ciao **{st.session_state['user'].email}** 👋")

    a = st.number_input("Base [m]", min_value=0.0, value=1.0)
    b = st.number_input("Altezza [m]", min_value=0.0, value=1.0)

    area = a * b
    st.success(f"L'area del rettangolo è **{area:.2f} m²**")

    st.button("Logout", on_click=logout)
