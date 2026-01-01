import streamlit as st
import requests

st.set_page_config(page_title="CodeSanctuary Prototype", layout="wide")

st.title("🧠 CodeSanctuary – AI-Assisted Code Recovery Prototype")
st.write("Simulates semantic recovery of broken code after outage or corruption.")

backend_url = st.text_input("Backend URL", "http://localhost:8000/recover/")

code_input = st.text_area("Paste broken code here:", height=200, placeholder="def broken_func():\n    print('missin bracket'")

if st.button("Analyze & Recover"):
    with st.spinner("Analyzing..."):
        resp = requests.post(backend_url, json={"broken_code": code_input})
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Suggested recovery source: **{data['suggested_file']}**")
            st.metric("Semantic similarity", f"{data['similarity_score']:.3f}")
        else:
            st.error("Backend error: could not connect or analyze.")
