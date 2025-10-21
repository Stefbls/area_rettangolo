import streamlit as st
from supabase import create_client, Client
import os

# --- CONFIGURAZIONE SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://<TUO_PROJECT>.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "<CHIAVE_ANON>")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIG STREAMLIT ---
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# --- CSS PERSONALIZZATO ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #2c3e50, #4ca1af);
    }
    .login-card {
        background-color: #fff;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.15);
        max-width: 400px;
        margin: auto;
    }
    .separator {
        text-align: center;
        border-bottom: 1px solid #ddd;
        line-height: 0.1em;
        margin: 25px 0 25px;
    }
    .separator span {
        background: #fff;
        padding: 0 10px;
        color: #888;
        font-size: 14px;
    }
    .google-btn {
        background-color: #fff;
        color: #555;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 8px 16px;
        text-align: center;
        width: 100%;
        font-weight: 500;
        display: block;
        margin-bottom: 8px;
    }
    .google-btn:hover {
        background-color: #f5f5f5;
    }
    .footer {
        text-align: center;
        margin-top: 25px;
        font-size: 13px;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSIONE ---
if "user" not in st.session_state:
    st.session_state["user"] = None

# --- LOGIN ---
if st.session_state["user"] is None:

    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>🔐 Log in</h2>", unsafe_allow_html=True)

    # --- LOGIN CON GOOGLE ---
    google_auth_url = f"{SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=http://localhost:8501"
    st.markdown(f"<a class='google-btn' href='{google_auth_url}'>Log in with Google</a>", unsafe_allow_html=True)

    st.markdown("<div class='separator'><span>or</span></div>", unsafe_allow_html=True)

    # Tabs per login/signup
    tab_login, tab_signup = st.tabs(["Login", "Sign up"])

    # --- LOGIN CON EMAIL ---
    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Log in"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state["user"] = res.user
                st.rerun()
            except Exception as e:
                st.error("❌ Email o password non valide.")

        st.markdown("<a href='#' style='font-size:13px; color:#2c7be5;'>Forgot your password?</a>", unsafe_allow_html=True)

    # --- SIGNUP NUOVO UTENTE ---
    with tab_signup:
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_pwd")

        if st.button("Sign up"):
            try:
                res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                if res.user:
                    st.success("✅ Registrazione completata! Controlla la tua email per confermare l'account.")
            except Exception as e:
                if "already registered" in str(e).lower():
                    st.warning("⚠️ Questa email è già registrata.")
                else:
                    st.error("Errore durante la registrazione.")

    st.markdown("<div class='footer'>Contact | Privacy | Terms of Use</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- APP AUTENTICATA ---
    st.title("📏 Calcolo area rettangolo")
    st.write(f"Benvenuto, **{st.session_state['user'].email}**")

    b = st.number_input("Base [cm]", min_value=0.0)
    h = st.number_input("Altezza [cm]", min_value=0.0)

    if b and h:
        st.success(f"L'area è {b * h:.2f} cm²")

    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state["user"] = None
        st.rerun()
