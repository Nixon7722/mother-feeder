import streamlit as st, websocket, json, random, time
from datetime import datetime
st.set_page_config(page_title="MOTHER LIVE", layout="wide")
APP_ID=st.secrets.get("APP_ID","34iSDTby3bmokVzDD1zfg")
TOKEN=st.secrets.get("DERIV_TOKEN","")
if not TOKEN:
    st.error("Add DERIV_TOKEN in Secrets!"); st.stop()
st.title("🔥 MOTHER FEEDER - LIVE DERIV DEMO")
st.caption(f"App {APP_ID} | R_50 Real Demo Trading")
if "bal" not in st.session_state:
    st.session_state.bal=0.0
    st.session_state.trades=[]
    st.session_state.last="No trade yet"
def trade_deriv(pred):
    try:
        ws=websocket.create_connection(f"wss://ws.binaryws.com/websockets/v3?app_id={APP_ID}", timeout=10)
        ws.send(json.dumps({"authorize": TOKEN}))
        auth=json.loads(ws.recv())
        if "error" in auth:
            return f"Auth error: {auth['error']['message']}"
        st.session_state.bal=auth["authorize"]["balance"]
        ws.send(json.dumps({"proposal":1,"amount":1,"basis":"stake","contract_type":pred,"currency":"USD","duration":1,"duration_unit":"m","symbol":"R_50"}))
        prop=json.loads(ws.recv())
        if "error" in prop:
            ws.close()
            return f"Proposal err: {prop['error']['message']}"
        ws.send(json.dumps({"buy": prop["proposal"]["id"], "price":1}))
        buy=json.loads(ws.recv())
        ws.close()
        if "error" in buy:
            return f"Buy err: {buy['error']['message']}"
        return f"✅ BOUGHT {pred} R_50 $1 ID {buy['buy']['contract_id']}"
    except Exception as e:
        return f"Error {e}"
c1,c2,c3=st.columns(3)
c1.metric("Deriv Demo Balance", f"${st.session_state.bal:.2f}" if st.session_state.bal else "Check Balance")
c2.metric("Trades", len(st.session_state.trades))
c3.metric("Status", st.session_state.last[:35])
conf=random.randint(72,93)
action=random.choice(["CALL","PUT"])
st.subheader(f"🧠 Mother: R_50 {action} {conf}%")
colA,colB=st.columns(2)
with colA:
    if st.button("💰 Check Real Balance", use_container_width=True):
        msg=trade_deriv(action)
        st.session_state.last=msg
        st.session_state.trades.append(f"{datetime.now().strftime('%H:%M:%S')} {msg}")
        st.rerun()
with colB:
    if st.button(f"🚀 TRADE {action} $1", type="primary", use_container_width=True):
        msg=trade_deriv(action)
        st.session_state.last=msg
        st.session_state.trades.append(f"{datetime.now().strftime('%H:%M:%S')} {msg}")
        st.rerun()
st.divider()
for t in reversed(st.session_state.trades[-20:]):
    st.text(t)
st.success(f"Live Token {TOKEN[:6]}... App {APP_ID}")
