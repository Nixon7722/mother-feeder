import streamlit as st
import json, os, random

st.set_page_config(page_title="MOTHER FEEDER", page_icon="🧬", layout="wide")

MEMORY_FILE = "mother_memory.json"
RULES_FILE = "survival_rules.json"
KEYS_FILE = "keys.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file) as f: return json.load(f)
        except: return default
    return default

def save_json(file, data):
    with open(file,'w') as f: json.dump(data,f,indent=2)

mem = load_json(MEMORY_FILE, {"total_trades":0,"children":[],"balance":10000,"history":[],"daily_loss":0})
rules = load_json(RULES_FILE, {"max_stake":0.35,"max_daily_loss":5.0,"death_balance":70,"reproduce_balance":115,"max_population":70,"parent_give":40,"min_confidence":70,"mutation_rate":5})
keys = load_json(KEYS_FILE, {"app_id":"","api_token":"","account_type":"demo"})

st.sidebar.title("🔑 Your Deriv Keys")
keys["app_id"] = st.sidebar.text_input("App ID", value=keys.get("app_id",""), placeholder="34iSDTby3bmokVzDD1zfg")
keys["api_token"] = st.sidebar.text_input("API Token", value=keys.get("api_token",""), type="password")
keys["account_type"] = st.sidebar.selectbox("Account", ["demo","real"], index=0)
keys["server"] = st.sidebar.selectbox("Market", ["R_50","R_10","R_25","R_75","R_100"], index=0)
if st.sidebar.button("💾 SAVE KEYS"):
    save_json(KEYS_FILE, keys)
    st.sidebar.success("Saved!")

st.sidebar.divider()
st.sidebar.title("⚙️ Survival Rules")
rules["max_stake"] = st.sidebar.number_input("Max Stake $", 0.10, 5.0, float(rules["max_stake"]), 0.05)
rules["max_daily_loss"] = st.sidebar.number_input("Max Daily Loss $", 1.0, 100.0, float(rules["max_daily_loss"]), 0.5)
rules["death_balance"] = st.sidebar.slider("Die if < %", 10, 90, int(rules["death_balance"]))
rules["reproduce_balance"] = st.sidebar.slider("Birth if > %", 101, 200, int(rules["reproduce_balance"]))
rules["max_population"] = st.sidebar.slider("Max Pop", 10, 200, int(rules["max_population"]))
rules["min_confidence"] = st.sidebar.slider("Min Confidence %", 50, 95, int(rules["min_confidence"]))
if st.sidebar.button("💾 SAVE RULES"):
    save_json(RULES_FILE, rules)
    st.sidebar.success("Rules saved!")

st.title("🧬 MOTHER FEEDER")
col1,col2,col3,col4 = st.columns(4)
col1.metric("Feeder Balance", f"${mem['balance']:.2f}")
col2.metric("Children", f"{len(mem['children'])}/{rules['max_population']}")
col3.metric("Daily Loss", f"${mem['daily_loss']:.2f}")
col4.metric("Trades", mem["total_trades"])

pred_conf = random.randint(68,94)
pred_action = "CALL" if random.random()>0.5 else "PUT"
can_trade = pred_conf >= rules["min_confidence"] and mem["daily_loss"] < rules["max_daily_loss"]

st.subheader(f"🧠 Prediction: {keys['server']} {pred_action} - {pred_conf}%")
if can_trade: st.success("✅ ALLOWED")
else: st.warning("Waiting for confidence or keys")

c1,c2,c3 = st.columns(3)
with c1:
    if st.button("👶 Birth Child", use_container_width=True):
        child = {"name":f"Child-{len(mem['children'])+1}","balance":100,"genes":{"risk":rules["max_stake"]/100},"children_count":0,"alive":True}
        mem["children"].append(child); mem["balance"]-=10; save_json(MEMORY_FILE, mem); st.rerun()
with c2:
    if st.button("▶️ Run Cycle", use_container_width=True, disabled=not can_trade):
        child = random.choice(mem["children"]) if mem["children"] else None
        if child:
            won = random.random() < pred_conf/100
            profit = rules["max_stake"]*0.9 if won else -rules["max_stake"]
            mem["balance"]+=profit
            if profit<0: mem["daily_loss"]+=abs(profit)
            mem["total_trades"]+=1; child["balance"]+= profit*10
            if child["balance"] < rules["death_balance"]: child["alive"]=False
            save_json(MEMORY_FILE, mem); st.rerun()
with c3:
    if st.button("🌅 Reset Day", use_container_width=True):
        mem["daily_loss"]=0; save_json(MEMORY_FILE, mem); st.rerun()

for ch in mem["children"][-10:]:
    st.text(f"{'✅' if ch['alive'] else '💀'} {ch['name']} Bal {ch['balance']:.1f}")
