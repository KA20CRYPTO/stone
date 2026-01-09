import streamlit as st
import random
import firebase_admin
from firebase_admin import credentials, db
import requests

if "user" not in st.session_state:
    st.session_state.user = None

# ---------- AUTH CONFIG ----------
FIREBASE_API_KEY = st.secrets["firebase_web"]["apiKey"]

def firebase_login(email, password):
    url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        f"?key={FIREBASE_API_KEY}"
    )
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    r = requests.post(url, json=payload)
    return r.json()

def firebase_signup(email, password):
    url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        f"?key={FIREBASE_API_KEY}"
    )
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    r = requests.post(url, json=payload)
    return r.json()

# Firebase init using Streamlit secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://stone-25ded-default-rtdb.firebaseio.com/"
    })

ref = db.reference("games")

st.set_page_config(page_title="Stone Paper Scissors", page_icon="✂️")
st.title("🪨📄✂️ Stone Paper Scissors")
st.subheader("🔐 Login / Sign Up")

if st.session_state.user is None:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            res = firebase_login(email, password)
            if "idToken" in res:
                st.session_state.user = {
                    "email": email,
                    "uid": res["localId"],
                    "token": res["idToken"]
                }
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error(res.get("error", {}).get("message", "Login failed"))

    with col2:
        if st.button("Sign Up"):
            res = firebase_signup(email, password)
            if "idToken" in res:
                st.success("Account created! Please log in.")
            else:
                st.error(res.get("error", {}).get("message", "Signup failed"))

    st.stop()

# -------- SIGN IN --------

player = st.session_state.user
st.write(f"👤 Logged in as: **{player}**")
# ---------- AUTH CONFIG ----------



player = st.text_input("Enter your name")

choices = ["Stone", "Paper", "Scissors"]
user_choice = st.radio("Choose one:", choices, horizontal=True)

if st.button("Play") and player:
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "Draw"
    elif (
        (user_choice == "Stone" and computer_choice == "Scissors") or
        (user_choice == "Paper" and computer_choice == "Stone") or
        (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        result = "Win"
    else:
        result = "Lose"

    st.success(f"Result: {result}")

    ref.push({
        "player": player,
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result
    })

