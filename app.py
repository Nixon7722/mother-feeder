import streamlit as st
import websocket, json, ssl

APP_ID = "34iR6HMxOfgO6m5LWOrAp"
TOKEN = "pat_7e7be64e69fe1920b567bab10a99835ba9a5fab6dcf059bfac5e6272da787002"

st.title("🔥 MOTHER FEEDER LIVE R_50")
st.caption(f"App {APP_ID} | Real Trading")

if st.button("💰 Check Real Balance"):
    try:
        ws = websocket.create_connection(f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}", sslopt={"cert_reqs": ssl.CERT_NONE}, timeout=10)
        ws.send(json.dumps({"authorize": TOKEN}))
        auth = json.loads(ws.recv())
        st.write(auth)
        if "error" in auth:
            st.error(f"Auth failed: {auth['error']['message']}")
        else:
            st.success(f"Authorized!")
            ws.send(json.dumps({"balance":1}))
            bal = json.loads(ws.recv())
            st.metric("Balance", f"${bal['balance']['balance']}")
            st.json(bal)
            ws.close()
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("🚀 TRADE R_50 CALL $1"):
    try:
        ws = websocket.create_connection(f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}", sslopt={"cert_reqs": ssl.CERT_NONE}, timeout=15)
        ws.send(json.dumps({"authorize": TOKEN}))
        auth = json.loads(ws.recv())
        if "error" in auth:
            st.error(auth['error']['message'])
        else:
            ws.send(json.dumps({"proposal":1,"amount":1,"basis":"stake","contract_type":"CALL","currency":"USD","duration":1,"duration_unit":"m","symbol":"R_50"}))
            prop = json.loads(ws.recv())
            st.write(prop)
            ws.send(json.dumps({"buy":prop['proposal']['id'],"price":1}))
            buy = json.loads(ws.recv())
            st.success(f"TRADE PLACED!")
            st.json(buy)
        ws.close()
    except Exception as e:
        st.error(str(e))
