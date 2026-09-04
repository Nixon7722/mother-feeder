import streamlit as st, requests

APP_ID = "34iR6HMxOfgO6m5LWOrAp"
TOKEN = "pat_7e7be64e69fe1920b567bab10a99835ba9a5fab6dcf059bfac5e6272da787002"

st.title("🔥 MOTHER FEEDER LIVE R_50")
st.caption(f"App {APP_ID} | Real Demo Trading")

if st.button("💰 Check Real Balance"):
    headers = {"Deriv-App-ID": APP_ID, "Authorization": f"Bearer {TOKEN}"}
    try:
        r = requests.get("https://api.deriv.com/trading/v1/options/accounts", headers=headers)
        st.write(f"Status: {r.status_code}")
        st.code(r.text[:2000])
        if r.status_code == 200:
            data = r.json()
            acc = data[0]
            st.success(f"Connected! Account: {acc['account_id']}")
            st.metric("Balance", acc.get('balance', 'N/A'))
            # get ws url
            r2 = requests.post(f"https://api.deriv.com/trading/v1/options/accounts/{acc['account_id']}/otp", headers=headers)
            st.write(f"OTP Status: {r2.status_code}")
            st.code(r2.text[:2000])
        else:
            st.error("Token expired - create new PAT token in Deriv Dashboard")
    except Exception as e:
        st.error(str(e))
