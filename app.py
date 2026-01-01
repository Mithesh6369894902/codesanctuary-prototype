import streamlit as st
import requests
from PIL import Image

# -------------------------------
# 🎨 Page Configuration
# -------------------------------
st.set_page_config(
    page_title="CodeSanctuary – AI Code Recovery",
    page_icon="🌐",
    layout="wide"
)

# -------------------------------
# 📂 Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2721/2721298.png",
        width=100,
        caption="CodeSanctuary"
    )
    st.title("⚙️ Navigation")

    page = st.radio(
        "Go to",
        ["Monitor", "Recovery Logs", "Settings"],
        index=0
    )

    st.markdown("---")
    st.markdown("**Status:** 🟢 Online")
    st.markdown("[View Project on GitHub](https://github.com/YOUR_GITHUB_USERNAME/codesanctuary-prototype)")
    st.caption("AI-powered semantic recovery for DevOps teams.")

# -------------------------------
# 🌐 Backend URL
# -------------------------------
backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000/recover/")

# -------------------------------
# 📊 MONITOR PAGE
# -------------------------------
if page == "Monitor":
    st.title("📡 Live Monitor")
    st.write(
        "Paste a broken or corrupted code snippet below to simulate AI recovery."
    )

    code_input = st.text_area(
        "Your broken code here:",
        height=200,
        placeholder="def broken_func():\n    print('missin bracket'"
    )

    if st.button("Analyze & Recover"):
        if not code_input.strip():
            st.warning("Please paste a code snippet to analyze.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    resp = requests.post(backend_url, json={"broken_code": code_input})
                    if resp.status_code == 200:
                        data = resp.json()
                        st.success(f"✅ Suggested recovery file: **{data['suggested_file']}**")
                        st.metric("Semantic similarity", f"{data['similarity_score']:.3f}")
                    else:
                        st.error(f"Backend error: {resp.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# -------------------------------
# 🧾 RECOVERY LOGS PAGE
# -------------------------------
elif page == "Recovery Logs":
    st.title("🧾 Recovery Logs")
    st.info(
        "In a real deployment, this page would show logs of all previous recovery attempts "
        "with timestamps, similarity scores, and results."
    )
    st.code(
        "Example log entry:\n"
        "[2026-01-01 10:14:03] File recovered: math_utils.py | Similarity: 0.872"
    )

# -------------------------------
# ⚙️ SETTINGS PAGE
# -------------------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Configure your backend and environment below:")

    new_url = st.text_input("Backend API URL:", backend_url)
    if st.button("Save"):
        st.success(f"Backend URL set to: {new_url}")
        st.balloons()

# -------------------------------
# 🧩 Footer
# -------------------------------
st.markdown("---")
st.caption("© 2026 CodeSanctuary Prototype • Built with Streamlit, FastAPI & CodeBERT")
