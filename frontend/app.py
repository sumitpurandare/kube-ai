import streamlit as st
import requests

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
        st.error("❌ Backend not reachable")
        return []


def fetch_data(namespace):
    try:
        url = f"{BACKEND_URL}/analyze-namespace/{namespace}"
        response = requests.get(url)
        return response.json()
    except:
        st.error("❌ Failed to fetch data")
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

st.sidebar.markdown("---")
st.sidebar.info("AI-powered Kubernetes Debugger")

# -----------------------
# Header
# -----------------------
st.markdown("## 🚀 KubeAI – Intelligent Kubernetes Debugger")
st.caption("AI-powered root cause analysis for Kubernetes workloads")

# -----------------------
# Main Logic
# -----------------------
if refresh:

    data = fetch_data(namespace)

    if not data or "total_pods" not in data:
        st.error("❌ Invalid backend response")
        st.stop()

    total = data["total_pods"]
    unhealthy = len([p for p in data["pods"] if p["status"] == "unhealthy"])
    healthy = total - unhealthy

    # -----------------------
    # Summary
    # -----------------------
    st.subheader("📊 Cluster Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pods", total)
    col2.metric("🟢 Healthy", healthy)
    col3.metric("🔴 Unhealthy", unhealthy)

    # 🔥 AI Summary Banner
    if unhealthy > 0:
        st.error(f"🚨 {unhealthy} pod(s) failing in namespace '{namespace}'")
    else:
        st.success("✅ All pods are healthy")

    st.markdown("---")

    # -----------------------
    # Pods View
    # -----------------------
    st.subheader("📦 Pods Status")

    pods = sorted(
        data["pods"],
        key=lambda x: x["status"] != "unhealthy"
    )

    for pod in pods:
        with st.container():
            col1, col2 = st.columns([3, 1])

            col1.markdown(f"### {pod['pod_name']}")

            if pod["status"] == "healthy":
                col2.success("🟢 Healthy")
            elif pod["status"] == "unhealthy":
                col2.error("🔴 Unhealthy")
            else:
                col2.warning("⚠️ Error")

            # -----------------------
            # Issues
            # -----------------------
            if pod["issues_found"]:
                with st.expander("🔍 Issues"):
                    for issue in pod["issues_found"]:
                        st.text(issue.get("message"))

            # -----------------------
            # AI Insights (🔥 Highlighted)
            # -----------------------
            if pod.get("ai_analysis"):
                ai = pod["ai_analysis"]

                with st.expander("🧠 AI Insight", expanded=True):
                    st.error(f"🚨 Issue: {ai.get('issue')}")
                    st.write(f"🔍 Root Cause: {ai.get('root_cause')}")
                    st.write(f"🛠 Fix: {ai.get('fix')}")
                    st.caption(f"Confidence: {ai.get('confidence')}%")

            st.markdown("---")

else:
    st.info("👉 Select namespace and click 'Analyze'")