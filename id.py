import streamlit as st
import requests

st.title("GET MY ACCOUNT ID")

APP_ID = "34iSDTby3bmokVzDD1zfg"
TOKEN = "pat_7e7be64e69fe1920b567bab10a99835ba9a5fab6dcf059bfac5e6272da787002"

if st.button("GET ID NOW"):
    headers = {
        "Deriv-App-ID": APP_ID,
        "Authorization": f"Bearer {TOKEN}"
    }
    r = requests.get("https://api.deriv.com/trading/v1/options/accounts", headers=headers)
    st.write(f"Status: {r.status_code}")
    st.json(r.json())
