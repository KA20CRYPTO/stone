import streamlit as st
import random
import firebase_admin
from firebase_admin import credentials, db

# Firebase init using Streamlit secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://stone-25ded-default-rtdb.firebaseio.com/"
    })

ref = db.reference("games")

st.set_page_config(page_title="Stone Paper Scissors", page_icon="✂️")
st.title("🪨📄✂️ Stone Paper Scissors")

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

