import streamlit as st
import requests

st.title("Get Account ID")

APP_ID = "34iSDTby3bmokVzDD1zfg"
TOKEN = "pat_7e7be64e69fe1920b567bab10a99835ba9a5fab6dcf059bfac5e6272da787002"

if st.button("GET ID NOW"):
    headers = {
        "Deriv-App-ID": APP_ID,
        "Authorization": f"Bearer {TOKEN}"
    }
    # Step 1
    url1 = "https://api.deriv.com/trading/v1/options/accounts"
    r1 = requests.get(url1, headers=headers)
    st.write("Step 1 Status:", r1.status_code)
    st.json(r1.json())

    data = r1.json()
    if isinstance(data, list) and len(data) > 0:
        acc_id = data[0]["account_id"]
        st.success(f"account_id = {acc_id}")

        # Step 2 - Get WS URL
        url2 = f"https://api.deriv.com/trading/v1/options/accounts/{acc_id}/otp"
        r2 = requests.post(url2, headers=headers)
        st.write("Step 2 OTP Response:")
        st.json(r2.json())
