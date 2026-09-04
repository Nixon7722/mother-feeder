import streamlit as st, requests, websocket, json, ssl

APP_ID="34iR6HMxOfgO6m5LWOrAp"
TOKEN="pat_6604c2a51cf0555cac31e30bff808ef704d7323e12594625f2e30a389b14e440"

st.title("🔥 MOTHER FEEDER LIVE R_50")
st.caption(f"App {APP_ID}")

if st.button("💰 Check Real Balance"):
    h={"Deriv-App-ID":APP_ID,"Authorization":f"Bearer {TOKEN}"}
    try:
        url="https://api.derivws.com/trading/v1/options/accounts"
        r1=requests.get(url,headers=h,timeout=15)
        st.write(f"Accounts: {r1.status_code}")
        st.code(r1.text[:3000])
        if r1.status_code==200:
            j=r1.json()
            accs=j.get("data",[])
            if not accs:
                st.error("No accounts found - create demo account in Deriv")
            else:
                acc=accs[0]
                st.success(f"Connected! {acc['account_id']}")
                st.metric("Balance", f"${acc['balance']} {acc['currency']} {acc['account_type']}")

                # get OTP
                r2=requests.post(f"https://api.derivws.com/trading/v1/options/accounts/{acc['account_id']}/otp",headers=h,timeout=15)
                st.write(f"OTP: {r2.status_code}")
                st.code(r2.text[:3000])
                if r2.status_code==200:
                    ws_url=r2.json()["data"]["url"]
                    st.session_state["ws_url"]=ws_url
                    st.session_state["acc_id"]=acc['account_id']
                    st.success("READY TO TRADE")
        else:
            st.error(r1.text)
    except Exception as e:
        st.error(str(e))

if st.button("🚀 TRADE R_50 CALL $1"):
    h={"Deriv-App-ID":APP_ID,"Authorization":f"Bearer {TOKEN}"}
    try:
        ws_url=st.session_state.get("ws_url")
        if not ws_url:
            st.warning("Tap Check Balance first")
        else:
            ws=websocket.create_connection(ws_url,sslopt={"cert_reqs":ssl.CERT_NONE},timeout=15)
            ws.send(json.dumps({"proposal":1,"amount":1,"basis":"stake","contract_type":"CALL","currency":"USD","duration":1,"duration_unit":"m","underlying_symbol":"R_50"}))
            p=json.loads(ws.recv())
            st.json(p)
            if "error" not in p:
                ws.send(json.dumps({"buy":p["proposal"]["id"],"price":p["proposal"]["ask_price"]}))
                b=json.loads(ws.recv())
                st.success("TRADE PLACED!")
                st.json(b)
                st.balloons()
            ws.close()
    except Exception as e:
        st.error(str(e))
