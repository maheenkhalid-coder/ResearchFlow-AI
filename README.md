# 🔎 ResearchFlow AI

### Multi-Agent AI Research & Analysis System

**ResearchFlow AI** is a multi-agent AI system that transforms a research question into a structured, source-backed report.

Instead of relying on a single LLM response, the system separates the research process into multiple specialized stages — **searching, reading, writing, and critical evaluation** — to produce more structured and reliable research outputs.

## 🚀 Live Demo

👉 **[Try ResearchFlow AI](https://6jqraysprgcj47fpbxkfvf.streamlit.app/)**

> The live demo is deployed using **Streamlit Community Cloud**.

---

## ✨ Features

* 🔎 **Web Search Agent** — finds recent and relevant sources using Tavily
* 📖 **Reader Agent** — retrieves and extracts deeper information from selected web pages
* ✍️ **Research Writer** — transforms gathered information into a structured research report
* 🧐 **Critic Agent** — evaluates the generated report for accuracy, completeness, clarity, reasoning, and source usage
* 🤖 **Multi-Agent Architecture** — separates research tasks across specialized AI agents
* 🌐 **Real Web Research** — uses live web sources instead of relying only on model knowledge
* 📑 **Structured Reports** — generates Introduction, Key Findings, Conclusion, and Sources
* ⚡ **Interactive Streamlit Interface** — simple interface for entering and researching any topic

---

## 🧠 How It Works

ResearchFlow AI follows a multi-stage research pipeline:

```text
                    User Research Question
                              │
                              ▼
                    ┌──────────────────┐
                    │   Search Agent   │
                    │                  │
                    │ Find relevant    │
                    │ web sources      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Reader Agent   │
                    │                  │
                    │ Scrape and read  │
                    │ selected source  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Research Writer │
                    │                  │
                    │ Generate report  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Critic Agent   │
                    │                  │
                    │ Evaluate report  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Final Report   │
                    └──────────────────┘
```

The goal is to demonstrate how multiple AI components can work together as a **research workflow**, rather than using one large language-model call for the entire task.

---

## 🏗️ Architecture

The current system consists of four major components:

### 1. Search Agent

The Search Agent receives the user's research topic and uses **Tavily** to find relevant web sources.

It returns information such as:

* Source title
* URL
* Search snippet

### 2. Reader Agent

The Reader Agent identifies a relevant source from the search results and uses a web-scraping tool to retrieve deeper page content.

The extracted content is cleaned using **BeautifulSoup** before being passed to the writer.

### 3. Research Writer

The Writer combines:

* Search results
* Scraped source content
* User's research topic

and generates a structured research report containing:

* Introduction
* Key Findings
* Conclusion
* Sources

### 4. Critic Agent

The Critic independently reviews the generated report and evaluates:

* Accuracy and factual support
* Completeness
* Clarity and structure
* Quality of reasoning
* Source usage

It then provides a score, strengths, areas for improvement, and an overall assessment.

---

## 🛠️ Tech Stack

### AI & LLM

* **Groq**
* **GPT-OSS-120B**
* **LangChain**

### Research & Web

* **Tavily**
* **Requests**
* **BeautifulSoup**

### Application

* **Python**
* **Streamlit**

### Deployment

* **Streamlit Community Cloud**

---

## 📂 Project Structure

```text
researchflow-ai/
│
├── backend/
│   ├── agents.py          # AI agents and LLM configuration
│   ├── pipeline.py        # Multi-agent research workflow
│   └── tools.py           # Web search and scraping tools
│
├── app.py                 # Streamlit application
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignored files and secrets
└── .env                   # Local API keys (not committed)
```

---

## ⚠️ Limitations

ResearchFlow AI is a portfolio and demonstration project.

The quality of the final report depends on:

* The quality and availability of web sources
* Web page accessibility
* Search results
* LLM-generated reasoning
* External API availability

The system should therefore be treated as a **research assistance tool**, not as a replacement for verifying important information against primary or authoritative sources.

---

## 👩‍💻 Project Purpose

This project was built to explore practical applications of:

* Large Language Models
* Multi-Agent AI systems
* Tool calling
* Web research automation
* Retrieval and information extraction
* AI-generated report writing
* LLM-based evaluation
* Agent orchestration

The main objective is to demonstrate how an AI system can decompose a complex research task into specialized steps and coordinate multiple agents to produce a final result.

