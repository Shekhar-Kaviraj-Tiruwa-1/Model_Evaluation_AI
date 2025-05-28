# 🧠 ModelEval.AI

> ⚖️ A real-time benchmarking platform for comparing outputs from multiple open-source Large Language Models (LLMs). Input once, compare instantly.

---

## 🚀 Project Overview

ModelEval.AI empowers developers and researchers to evaluate multiple LLMs in parallel using a single prompt. Built on AI Engineering best practices (inspired by Chip Huyen's book), it brings A-to-Z production-readiness, model transparency, and rich evaluation metrics to LLM benchmarking.

---

## 🎯 Key Features

- 🔁 Real-time multi-model response generation
- 📊 Evaluation using BERTScore, ROUGE, and custom metrics
- 🏆 Leaderboard and scoring insights
- 🧩 Modular and production-ready architecture
- 🌐 Local & cloud-friendly deployment

---

## 🧱 Architecture Overview

mermaid
graph TD
- UI[Web Interface (Streamlit/FastAPI)]
- Prompt[User Prompt]
- Engine[LLM Inference Engine]
- odels[Mistral, LLaMA, DeepSeek]
- Eval[Evaluation Metrics]
- DB[(MongoDB + FAISS)]
- Dashboard[Monitoring & Leaderboard]

    UI --> Prompt
    Prompt --> Engine
    Engine --> Models
    Models --> Eval
    Eval --> DB
    DB --> Dashboard
    Eval --> UI
