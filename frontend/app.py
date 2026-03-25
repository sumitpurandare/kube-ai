import streamlit as st
import subprocess
import requests
from src.services.api import analyze_logs  # old flow (kept)

st.set_page_config(page_title="K8s AI Analyzer", layout="wide")

# -----------------------
# Helper functions
# -----------------------
def get_namespaces():
    result = subprocess.run(
        ["kubectl", "get", "ns", "-o", "jsonpath={.items[*].metadata.name}"],
        capture_output=True, text=True
    )
    return result.stdout.split() if result.stdout else []

def get_pods(namespace: str):
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-o", "jsonpath={.items[*].metadata.name}"],
        capture_output=True, text=True
    )
    return result.stdout.split() if result.stdout else []

def fetch_logs(pod: str, namespace: str):
    result = subprocess.run(
        ["kubectl", "logs", pod, "-n", namespace],
        capture_output=True, text=True
    )
    return result.stdout if result.stdout else "No logs found"

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("⚙️ Settings")

namespaces = get_namespaces()
selected_ns = st.sidebar.selectbox("Namespace", namespaces) if namespaces else "default"

pods = get_pods(selected_ns)
selected_pod = st.sidebar.selectbox("Pod", pods) if pods else ""

mode = st.sidebar.selectbox(
    "Mode",
    ["Paste Logs", "Fetch Pod Logs", "Namespace Analysis (🚀)"]
)

st.sidebar.markdown("---")
st.sidebar.info("Analyze Kubernetes issues instantly")

# -----------------------
# Logs Input Section
# -----------------------
st.title("🚀 AI Kubernetes Log Analyzer")

if mode in ["Paste Logs", "Fetch Pod Logs"]:
    st.subheader("📥 Input Logs")

    if mode == "Paste Logs":
        logs = st.text_area("Paste your logs here", height=250)
    else:
        logs = fetch_logs(selected_pod, selected_ns)
        st.text_area(f"Logs from pod '{selected_pod}'", logs, height=300)

    if not logs:
        st.info("👆 Provide logs and click Analyze")

# -----------------------
# Analyze Button
# -----------------------
if st.button("🔍 Analyze"):

    # =====================================================
    # 🚀 NEW: Namespace Analysis (REAL PRODUCT FEATURE)
    # =====================================================
    if mode == "Namespace Analysis (🚀)":

        with st.spinner("Analyzing entire namespace..."):
            url = f"http://127.0.0.1:8000/analyze-namespace/{selected_ns}"
            response = requests.get(url)
            data = response.json()

        st.subheader(f"📦 Namespace: {data['namespace']}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Pods", data["total_pods"])

        total_issues = sum(len(p.get("issues_found", [])) for p in data["pods"])
        with col2:
            st.metric("Total Issues", total_issues)

        st.markdown("---")

        # Sort pods: problematic first
        pods_sorted = sorted(
            data["pods"],
            key=lambda x: len(x.get("issues_found", [])),
            reverse=True
        )

        for pod in pods_sorted:
            pod_name = pod["pod_name"]
            issues = pod.get("issues_found", [])

            if issues:
                st.error(f"🔴 {pod_name} - {len(issues)} issue(s)")
            else:
                st.success(f"🟢 {pod_name} - Healthy")

            with st.expander(f"Details: {pod_name}"):

                if issues:
                    for issue in issues:
                        st.code(issue)
                else:
                    st.write("No issues detected ✅")

    # =====================================================
    # 🟡 OLD FLOW: Single Log Analysis
    # =====================================================
    else:
        if not logs.strip():
            st.warning("Please provide logs first")
        else:
            with st.spinner("Analyzing logs..."):
                result = analyze_logs(logs)

            st.subheader("📊 Analysis Result")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🚨 Issue", result.get("issue", result.get("summary", "N/A")))
                st.metric("📊 Confidence", f"{result.get('confidence', 0)}%")

            with col2:
                st.metric("🧠 Root Cause", result.get("root_cause", "N/A"))

            st.markdown("### 🛠 Recommended Fix")
            st.success(result.get("fix", result.get("priority_action", "No suggestion available")))