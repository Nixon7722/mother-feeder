import streamlit as st
import requests
import websocket
import json
import threading

APP_ID = "34iSDTby3bmokVzDD1zfg"
TOKEN = "pat_7e7be64e69fe1920b567bab10a99835ba9a5fab6dcf059bfac5e6272da787002"

st.title("🔥 MOTHER FEEDER - LIVE DERIV DEMO")
st.caption(f"App {APP_ID} | R_50 Real Demo Trading")

balance_text = st.empty()
status_text = st.empty()

if "trades" not in st.session_state:
    st.session_state.trades = 0

st.write(f"Trades\n{st.session_state.trades}")
st.write(f"Status\nNo trade yet")

st.markdown("### 🧠 Mother: R_50 CALL 93%")

def get_otp_url():
    headers = {"Deriv-App-ID": APP_ID, "Authorization": f"Bearer {TOKEN}"}
    r1 = requests.get("https://api.deriv.com/trading/v1/options/accounts", headers=headers)
    acc_id = r1.json()[0]["account_id"]
    r2 = requests.post(f"https://api.deriv.com/trading/v1/options/accounts/{acc_id}/otp", headers=headers)
    ws_url = r2.json()["data"]["url"]
    return ws_url, acc_id

if st.button("💰 Check Real Balance"):
    try:
        ws_url, acc_id = get_otp_url()
        st.success(f"Connected! Account: {acc_id}")
        st.code(ws_url)

        # Now connect to that ws_url
        def on_message(ws, msg):
            data = json.loads(msg)
            if "balance" in data:
                balance_text.markdown(f"## Deriv Demo Balance\n{data['balance']['balance']}")

        ws = websocket.WebSocketApp(ws_url, on_message=on_message)
        ws.run_forever()
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("🚀 TRADE CALL $1"):
    st.session_state.trades += 1
    st.write("Placing R_50 CALL $1...")

st.success(f"Live Token pat_7e... App {APP_ID}")
