# 🚀 KubeAI – AI-Powered Kubernetes Debugger

KubeAI is an AI-powered observability tool that analyzes Kubernetes logs in real-time and provides automated issue detection, root cause analysis, and fix recommendations. Instead of manually scanning logs, KubeAI helps you instantly understand what went wrong and how to fix it.

---

## 🧠 Features

- 📦 Namespace-based pod analysis  
- 🔴 Automatic unhealthy pod detection  
- 🧠 AI insights (issue, root cause, fix)  
- 📊 Interactive Streamlit dashboard  
- ⚙️ CLI tool for log analysis  
- 🔗 Kubernetes integration via kubectl  

---

## 🏗️ Architecture

Kubernetes Cluster → Pod Logs (kubectl) → Log Parser + AI Analyzer → FastAPI Backend → Streamlit UI Dashboard

---

## 🧪 Example

Pod: sample-fastapi  
Status: Unhealthy  

AI Insight:  
- Issue: Application error  
- Root Cause: Runtime exception detected  
- Fix: Check logs and stack trace  

---

## 📂 Project Structure

kube-ai/  
├── kube-ai-analyzer/   (Core engine: parser + AI)  
├── backend/            (FastAPI backend)  
├── frontend/           (Streamlit UI)  
├── k8s/                (Kubernetes manifests)  

---

## 🚀 Getting Started

Clone repository:

git clone https://github.com/your-username/kube-ai.git  
cd kube-ai  

Setup Backend:

cd backend  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
pip install -e ../kube-ai-analyzer  
python -m uvicorn app.main:app --reload  

Setup Frontend:

cd ../frontend  
python3 -m venv venv  
source venv/bin/activate  
pip install streamlit requests  
streamlit run app.py  

Deploy Sample App:

kubectl apply -f k8s/sample-fastapi.yaml  

Run Analysis:

Open UI → select namespace → click Analyze → view AI insights  

---

## 🧠 How It Works

1. Logs are collected from Kubernetes pods  
2. Logs are parsed into structured format  
3. Errors are detected (ERROR, CrashLoopBackOff, etc.)  
4. AI generates issue, root cause, and fix  

---

## 🔥 Example Output

{
  "pod_name": "sample-fastapi",
  "status": "unhealthy",
  "issues_found": [...],
  "ai_analysis": {
    "issue": "Application error",
    "root_cause": "Runtime exception detected",
    "fix": "Check logs and stack trace",
    "confidence": 70
  }
}

---

## 💡 Use Cases

- DevOps debugging  
- Kubernetes monitoring  
- Incident triaging  
- Log analysis automation  

---

## 🚀 Future Improvements

- LLM integration (OpenAI / local models)  
- Multi-cluster support  
- Historical analysis  
- Alerting system  

---

## 👨‍💻 Author

Sumit Purandare  
DevOps Engineer | AI + Kubernetes Enthusiast  

---

## ⭐ Why this project matters

KubeAI shows how AI can simplify Kubernetes debugging by reducing manual log analysis and improving incident response time.

---