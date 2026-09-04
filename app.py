import streamlit as st, requests, websocket, json, ssl

APP_ID="34iR6HMxOfgO6m5LWOrAp"
TOKEN="pat_6604c2a51cf0555cac31e30bff808ef704d7323e12594625f2e30a389b14e440"

st.title("🔥 MOTHER FEEDER LIVE R_50")
st.caption(f"App {APP_ID} | Real Trading Ready")

if st.button("💰 Check Real Balance"):
    h={"Deriv-App-ID":APP_ID,"Authorization":f"Bearer {TOKEN}"}
    try:
        r1=requests.get("https://api.deriv.com/trading/v1/options/accounts",headers=h,timeout=15)
        st.write(f"Accounts: {r1.status_code}")
        if r1.status_code!=200:
            st.error(r1.text)
        else:
            acc=r1.json()[0]
            acc_id=acc["account_id"]
            st.success(f"Connected! {acc_id}")
            st.metric("Balance", f"${acc.get('balance')} {acc.get('currency')}")
            st.json(acc)

            r2=requests.post(f"https://api.deriv.com/trading/v1/options/accounts/{acc_id}/otp",headers=h,timeout=15)
            st.write(f"OTP: {r2.status_code}")
            if r2.status_code==200:
                ws_url=r2.json()["data"]["url"]
                st.code(ws_url[:200]+"...")
                st.session_state["ws_url"]=ws_url
                st.session_state["acc_id"]=acc_id
                st.success("READY TO TRADE - Tap TRADE button below")
            else:
                st.error(r2.text)
    except Exception as e:
        st.error(str(e))

if st.button("🚀 TRADE R_50 CALL $1"):
    h={"Deriv-App-ID":APP_ID,"Authorization":f"Bearer {TOKEN}"}
    try:
        acc_id=st.session_state.get("acc_id")
        if not acc_id:
            r1=requests.get("https://api.deriv.com/trading/v1/options/accounts",headers=h,timeout=10)
            acc_id=r1.json()[0]["account_id"]
            r2=requests.post(f"https://api.deriv.com/trading/v1/options/accounts/{acc_id}/otp",headers=h,timeout=10)
            ws_url=r2.json()["data"]["url"]
        else:
            ws_url=st.session_state["ws_url"]

        st.write(f"Connecting to {ws_url[:80]}...")
        ws=websocket.create_connection(ws_url,sslopt={"cert_reqs":ssl.CERT_NONE},timeout=15)

        # proposal
        ws.send(json.dumps({"proposal":1,"amount":1,"basis":"stake","contract_type":"CALL","currency":"USD","duration":1,"duration_unit":"m","underlying_symbol":"R_50"}))
        p=json.loads(ws.recv())
        st.json(p)

        if "error" in p:
            st.error(p["error"]["message"])
        else:
            ws.send(json.dumps({"buy":p["proposal"]["id"],"price":p["proposal"]["ask_price"]}))
            b=json.loads(ws.recv())
            st.success("TRADE PLACED LIVE!")
            st.json(b)
            st.balloons()
        ws.close()
    except Exception as e:
        st.error(f"Trade Error: {e}")
