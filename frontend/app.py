import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="K8s AI Analyzer", layout="wide")

# -----------------------
# API Helpers
# -----------------------
def get_namespaces():
    try:
        res = requests.get(f"{BACKEND_URL}/namespaces")
        return res.json().get("namespaces", [])
    except:
        return []


def fetch_data(namespace):
    try:
        url = f"{BACKEND_URL}/analyze-namespace/{namespace}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return response.json()
    except:
        return None


# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("⚙️ Settings")

namespaces = get_namespaces()

if namespaces:
    namespace = st.sidebar.selectbox("Namespace", namespaces)
else:
    namespace = st.sidebar.text_input("Namespace", "default")

refresh = st.sidebar.button("🔄 Analyze")

# 🔥 Features
show_only_unhealthy = st.sidebar.checkbox("🔴 Show only unhealthy pods")
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh")
refresh_interval = st.sidebar.slider("Refresh Interval (sec)", 5, 60, 10)

st.sidebar.markdown("---")
st.sidebar.info("AI-powered Kubernetes Debugger")

# -----------------------
# Header
# -----------------------
st.markdown("## 🚀 KubeAI – Intelligent Kubernetes Debugger")
st.caption("AI-powered root cause analysis for Kubernetes workloads")

# 🔥 Timestamp (auto-refresh visibility)
st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")

# -----------------------
# Always Load Data
# -----------------------
data = fetch_data(namespace)

# -----------------------
# Safe Handling
# -----------------------
if data is None:
    st.warning("⏳ Waiting for backend...")
    st.stop()

if not isinstance(data, dict) or "total_pods" not in data:
    st.error("❌ Invalid backend response")
    st.stop()

# -----------------------
# Process Data
# -----------------------
total = data["total_pods"]
unhealthy = len([p for p in data["pods"] if p["status"] == "unhealthy"])
healthy = total - unhealthy

# -----------------------
# 📊 Cluster Summary
# -----------------------
st.subheader("📊 Cluster Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Pods", total)
col2.metric("🟢 Healthy", healthy)
col3.metric("🔴 Unhealthy", unhealthy)

# -----------------------
# 🧠 AI Summary
# -----------------------
if unhealthy > 0:
    st.warning(f"⚠️ System has {unhealthy} failing pod(s). Immediate attention required.")
else:
    st.success("✅ System is stable. No issues detected.")

# -----------------------
# 🚨 Top Issues Panel
# -----------------------
st.subheader("🚨 Top Issues")

if unhealthy > 0:
    failing_pods = [p for p in data["pods"] if p["status"] == "unhealthy"]

    for pod in failing_pods:
        ai = pod.get("ai_analysis")
        if ai:
            st.error(f"{pod['pod_name']} → {ai.get('issue')}")
        else:
            st.warning(f"{pod['pod_name']} → Unknown issue")
else:
    st.success("No critical issues detected 🎉")

st.markdown("---")

# -----------------------
# 📦 Pods View
# -----------------------
st.subheader("📦 Pods Status")

pods = sorted(
    data["pods"],
    key=lambda x: x["status"] != "unhealthy"
)

# 🔥 Filter
if show_only_unhealthy:
    pods = [p for p in pods if p["status"] == "unhealthy"]

for pod in pods:
    with st.container(border=True):

        col1, col2 = st.columns([3, 1])

        col1.markdown(f"### {pod['pod_name']}")

        if pod["status"] == "unhealthy":
            col2.error("🔴 CRITICAL")
        elif pod["status"] == "healthy":
            col2.success("🟢 Healthy")
        else:
            col2.warning("⚠️ Error")

        # -----------------------
        # Issues
        # -----------------------
        if pod["issues_found"]:
            with st.expander("🔍 Issues"):
                for issue in pod["issues_found"]:
                    level = issue.get("level", "INFO")
                    msg = issue.get("message")

                    if level == "CRITICAL":
                        st.error(msg)
                    elif level == "WARNING":
                        st.warning(msg)
                    else:
                        st.info(msg)

        # -----------------------
        # AI Insights
        # -----------------------
        if pod.get("ai_analysis"):
            ai = pod["ai_analysis"]

            with st.expander("🧠 AI Insight", expanded=True):
                st.error(f"🚨 Issue: {ai.get('issue')}")
                st.write(f"🔍 Root Cause: {ai.get('root_cause')}")
                st.write(f"🛠 Fix: {ai.get('fix')}")
                st.caption(f"Confidence: {ai.get('confidence')}%")

# -----------------------
# 🔄 Manual Refresh
# -----------------------
if refresh:
    st.rerun()

# -----------------------
# 🔄 Auto Refresh
# -----------------------
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()