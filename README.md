# 🚀 Kube-AI: AI-Powered Kubernetes Log Analyzer

## 📌 Project Overview

Kube-AI is a local-first SaaS prototype that analyzes Kubernetes logs and provides intelligent insights such as:

- Root cause of failures
- Possible reasons
- Suggested fixes

This project is built using:
- Kubernetes (Minikube)
- FastAPI (Backend + AI Engine)
- Docker (containerization)

---

## 🧠 Architecture

Client (curl/Postman)
        |
        v
   Backend API
        |
        v
    AI Engine
        |
        v
 Log Analysis Logic

---

## 📁 Project Structure

kube-ai/
├── ai-engine/
│   ├── app/
│   │   ├── main.py
│   │   └── analyzer.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/
│   ├── namespace.yaml
│   ├── ai-engine/
│   ├── backend/
│
└── README.md

---

## ⚙️ What Each Component Does

### 🔹 AI Engine
- Accepts logs
- Detects issues like:
  - CrashLoopBackOff
  - OOMKilled
  - ImagePullBackOff
- Returns structured analysis

### 🔹 Backend
- Accepts file upload (`/analyze`)
- Sends logs to AI Engine
- Returns response to user

### 🔹 Kubernetes
- Runs services as pods
- Handles networking between services
- Exposes backend externally

---

## 🚀 Setup & Execution Steps

### 1️⃣ Start Minikube

minikube start --driver=docker

---

### 2️⃣ Point Docker to Minikube

eval $(minikube docker-env)

---

### 3️⃣ Build Docker Images

docker build -t ai-engine:v1 ./ai-engine
docker build -t backend:v1 ./backend

---

### 4️⃣ Deploy to Kubernetes

kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/ai-engine/
kubectl apply -f k8s/backend/

---

### 5️⃣ Verify Pods

kubectl get pods -n kube-ai

Expected:
ai-engine-xxxxx   Running
backend-xxxxx     Running

---

### 6️⃣ Expose Backend Service

minikube service backend-service -n kube-ai

---

## 🧪 Testing the API

### Create sample log file

echo "CrashLoopBackOff error in pod nginx" > sample.log

---

### Call API

curl -X POST http://127.0.0.1:<PORT>/analyze \
  -F "file=@sample.log"

---

### ✅ Expected Response

{
  "result": {
    "analysis": {
      "issue": "Pod CrashLoopBackOff",
      "reason": "Container keeps restarting",
      "suggestion": "Check container logs and startup commands"
    }
  }
}

---

## 🔄 How to Update Code

1. Make changes (e.g. analyzer.py)

2. Rebuild image

docker build -t ai-engine:v1 ./ai-engine

3. Restart deployment

kubectl rollout restart deployment ai-engine -n kube-ai

4. Test again

---

## 🐞 Issues Faced & Fixes

❌ Minikube stuck pulling image  
✔ Fixed using retry / patience / mirrors  

❌ Docker daemon connection error  
✔ Fixed using:  
eval $(minikube docker-env -u)

❌ ContainerCreating stuck  
✔ Fixed using:  
imagePullPolicy: Never

❌ CNI / networking errors  
✔ Fixed by resetting Minikube and Docker  

---

## 🧠 Key Learnings

- Kubernetes does NOT auto-reload code
- Images must be rebuilt and redeployed
- Service-to-service communication uses DNS
- Debugging requires checking:
  - pods
  - logs
  - events

---

## 🔥 What We Built

- Microservices architecture
- Internal service communication
- AI-powered log analyzer (basic)
- Kubernetes deployment from scratch

---

## 🚀 Next Steps

- Improve AI logic (real log parsing)
- Add frontend UI
- Add authentication (multi-user SaaS)
- Connect to real Kubernetes logs
- Add LLM-based analysis

---

## 💡 Goal

Turn this into a real SaaS product for:

- Kubernetes debugging  
- DevOps automation  
- AI-assisted root cause analysis  

---

## 🙌 Status

✅ Working end-to-end on local Kubernetes  
🚧 Improving intelligence and features next  


SAAS model:
                🌐 USER (DevOps Engineer)
                         │
                         ▼
                ┌───────────────────┐
                │   Frontend (UI)   │
                │ Streamlit / React │
                └───────────────────┘
                         │
                         ▼
                ┌───────────────────┐
                │   API Gateway     │
                │  (NGINX / LB)     │
                └───────────────────┘
                         │
                         ▼
                ┌───────────────────┐
                │ FastAPI Backend   │
                │  (AI Engine)      │
                └───────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Kubernetes   │  │ PostgreSQL   │  │ Object Store │
│ Clusters     │  │ (Metadata)   │  │ (S3 Logs)    │
└──────────────┘  └──────────────┘  └──────────────┘
        │
        ▼
┌──────────────────────┐
│ Kube-AI Agent (opt)  │
│ (Log Collector)      │
└──────────────────────┘


AWS model
                🌍 Internet
                     │
                     ▼
        ┌──────────────────────────┐
        │  AWS ALB (Load Balancer) │
        └──────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │  FastAPI (EC2 / EKS)     │
        └──────────────────────────┘
             │            │
             ▼            ▼
   ┌──────────────┐   ┌──────────────┐
   │ RDS Postgres │   │   S3 Bucket  │
   └──────────────┘   └──────────────┘
             │
             ▼
   ┌──────────────────────┐
   │ External K8s Clusters│
   └──────────────────────┘


   