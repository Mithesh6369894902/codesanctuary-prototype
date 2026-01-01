import streamlit as st
import requests
import sqlite3
import pandas as pd
import time
import random
from datetime import datetime
import plotly.express as px

# -------------------------------
# 🎨 Page Configuration
# -------------------------------
st.set_page_config(
    page_title="CodeSanctuary – AI Code Recovery",
    page_icon="🔒",
    layout="wide"
)

# -------------------------------
# 💾 Database Setup
# -------------------------------
def init_db():
    conn = sqlite3.connect("recovery_logs.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recovery_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            file_suggested TEXT,
            similarity_score REAL,
            status TEXT
        )
    """)
    conn.commit()
    return conn

conn = init_db()

def log_recovery(file_name, score, status="Success"):
    conn.execute(
        "INSERT INTO recovery_logs (timestamp, file_suggested, similarity_score, status) VALUES (?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_name, score, status)
    )
    conn.commit()

def get_logs():
    df = pd.read_sql_query("SELECT * FROM recovery_logs ORDER BY id DESC", conn)
    return df

# -------------------------------
# 📂 Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2721/2721298.png", width=100)
    st.title("🧠 CodeSanctuary")
    page = st.radio("📍 Navigation", ["Monitor", "Recovery Logs", "Settings"], index=0)
    st.markdown("---")
    st.markdown("**Status:** 🟢 Online")
    st.caption("AI-Powered Code Recovery Dashboard")

# -------------------------------
# 🌐 Backend URL
# -------------------------------
backend_url = st.secrets.get("BACKEND_URL", "http://localhost:8000/recover/")

# -------------------------------
# 📡 MONITOR PAGE
# -------------------------------
if page == "Monitor":
    st.title("📡 Live Monitor – Recovery Simulation")

    code_input = st.text_area(
        "Paste broken code here:",
        height=200,
        placeholder="def broken_func():\n    print('missin bracket'"
    )

    if st.button("Analyze & Recover"):
        if not code_input.strip():
            st.warning("Please paste a code snippet to analyze.")
        else:
            with st.spinner("Analyzing and recovering..."):
                # Simulate live progress updates
                progress = st.progress(0)
                chart_data = pd.DataFrame({"Step": [], "Confidence": []})
                chart_placeholder = st.empty()

                for pct in range(0, 101, 10):
                    progress.progress(pct)
                    time.sleep(0.2)
                    chart_data = pd.concat(
                        [chart_data, pd.DataFrame({"Step": [pct], "Confidence": [random.uniform(0.4, 0.99)]})],
                        ignore_index=True
                    )
                    fig = px.line(chart_data, x="Step", y="Confidence",
                                  title="Real-time Recovery Confidence",
                                  range_y=[0, 1], markers=True)
                    chart_placeholder.plotly_chart(fig, use_container_width=True)

                # Send to backend
                try:
                    resp = requests.post(backend_url, json={"broken_code": code_input})
                    if resp.status_code == 200:
                        data = resp.json()
                        st.success(f"✅ Suggested recovery file: **{data['suggested_file']}**")
                        st.metric("Semantic similarity", f"{data['similarity_score']:.3f}")
                        log_recovery(data["suggested_file"], data["similarity_score"], "Success")
                    else:
                        st.error(f"Backend error: {resp.status_code}")
                        log_recovery("N/A", 0, "Failed")
                except Exception as e:
                    st.error(f"Connection error: {e}")
                    log_recovery("N/A", 0, "Connection Error")

# -------------------------------
# 🧾 RECOVERY LOGS PAGE
# -------------------------------
elif page == "Recovery Logs":
    st.title("🧾 Recovery Logs Database")
    df = get_logs()

    if df.empty:
        st.info("No recovery attempts logged yet.")
    else:
        st.dataframe(df, use_container_width=True)

        avg_score = df["similarity_score"].mean()
        success_rate = (df["status"] == "Success").mean() * 100

        col1, col2 = st.columns(2)
        col1.metric("Average Similarity", f"{avg_score:.3f}")
        col2.metric("Success Rate", f"{success_rate:.1f}%")

        fig = px.bar(df, x="timestamp", y="similarity_score",
                     color="status", title="Similarity Scores over Time")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# ⚙️ SETTINGS PAGE
# -------------------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    new_url = st.text_input("Backend API URL:", backend_url)
    if st.button("Save"):
        st.success(f"Backend URL set to: {new_url}")
        st.balloons()

# -------------------------------
# 🧩 Footer
# -------------------------------
st.markdown("---")
st.caption("🧠 CodeSanctuary © 2026 • 💾 AI-Driven Code Recovery & Monitoring Dashboard")

