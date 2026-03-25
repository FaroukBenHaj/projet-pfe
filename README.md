#  End of studies project :

> An intelligent security intelligence platform that makes vulnerability management accessible for everyone not just security experts.

---

## What is the project ?

It is a two-agent AI system built on top of DefectDojo that bridges the gap between penetration testing teams and the stakeholders who need to act on their findings. It introduces two specialized agents powered by Large Language Models — a **Tester Agent** for security professionals and a **Client Agent** for non-technical stakeholders — connected to DefectDojo in real time via the Model Context Protocol (MCP).

The core idea is simple: security data should speak the language of whoever is reading it. For a pentester, that means speed, power, and a live visual map . For a CEO or product owner, that means plain-language briefings and business consequences.

---

## The problem it solves

Vulnerability Management Platforms like DefectDojo are built exclusively for security experts. Non-technical clients — managers, CEOs, product owners — are completely excluded from the workflow. They receive raw findings they can't interpret, in interfaces they can't navigate, without any understanding of what the data means for their business.

At the same time, existing AI tools in cybersecurity (PentestGPT, HackerGPT) are disconnected from vulnerability management workflows entirely. They can answer security questions, but they can't read, create, or update findings inside a VMS.

the project  fills both gaps simultaneously.

---

## Architecture overview

This project is built around a shared knowledge graph that sits at the center of the system. The Tester Agent builds it. The Client Agent reads from it.

```
![Diagram global](Documents/Images/architecture.jpg)
```

### Core components

| Component | Role |
|---|---|
| **Tester Agent** | Processes natural language commands, writes findings to DefectDojo, enriches the knowledge graph |
| **Client Agent** | Reads the knowledge graph, generates business-consequence narratives, powers the Security Mirror |
| **Knowledge Graph** | Shared relational brain — findings, assets, CWEs, CVSS chains, exploitation paths |
| **RAG Module** | Documentary knowledge layer — OWASP, CWE descriptions, CVSS guidelines, remediation references |
| **MCP Server** | Bridge between the LLM agents and DefectDojo's REST API |
| **DefectDojo** | Source of truth for raw findings data, deployed via Docker |
| **FastAPI Backend** | Async API handling routing, authentication, and LLM streaming |
| **PostgreSQL** | Session storage, conversation history, business context profiles |

---

## The Tester Agent

The Tester Agent gives pentesters a natural language interface to DefectDojo. Instead of navigating complex forms and dashboards, the pentester types commands in plain English and the agent handles everything.

### Interface

The tester works in a split-screen workspace:

- **Left panel — Chatbot**: natural language commands and queries
- **Right panel — Switchable view**: three ways to visualize the same data
  - **Graph view** — live knowledge graph showing findings, assets, and exploitation chains as connected nodes
  - **Cards view** — each finding as a clean card with severity badge, asset, and plain description
  - **List view** — sortable table filtered by severity, status, or asset

### What it does

- Accepts natural language commands: *"add a critical SQL injection to the payment service"*
- Writes the finding to DefectDojo via the MCP Server
- Simultaneously enriches the knowledge graph — creating nodes, linking to assets, connecting to CWE categories, detecting related findings and exploitation chains
- On first login, automatically ingests all existing DefectDojo findings and builds the initial knowledge graph
- Detects emerging patterns: clusters of findings on the same asset, forming exploitation chains, escalating risk on a specific service
- Answers graph questions in plain language: *"which asset has the most critical findings?"*, *"is there an exploitation chain in this project?"*

---

## The Client Agent — Security Mirror

The Client Agent is not a chatbot. It is a proactive intelligence dashboard called the **Security Mirror** that speaks first — the agent has already analyzed the latest findings and prepared a briefing before the client types anything.

### First login — business context onboarding

On first login, the agent interviews the client with plain-language questions: what does your company do, who are your users, what data do you store, what regulations apply to you. This profile is saved and used to personalize every response from that point forward. Onboarding happens once.

### The dashboard

When the client logs in they land on the Security Mirror with five sections:

1. **Greeting** — personalized, timestamped, already telling the client what changed
2. **Live briefing** — a proactive plain-language narrative prepared by the agent, no input required. Key facts bolded. Action buttons pre-seeded with the most relevant follow-up questions.
3. **Metrics row** — open findings count, findings fixed this week, estimated exposure window
4. **Findings list** — each finding translated into a one-sentence business consequence. Tapping any row opens a conversation with that finding's context already loaded.
5. **Ask your advisor** — chat input with contextually generated quick-question chips at the bottom

### Business Risk Index

A single number between 0 and 100, updated in real time as findings are added, closed, or escalated. Not a CVSS average — a business risk score the CEO can track week over week without reading a single report.

---

## Knowledge graph vs RAG — the two-layer knowledge system

| Layer | Technology | Handles |
|---|---|---|
| **Knowledge graph** | Neo4j | Structured, relational, live data — findings, assets, CWEs, exploitation chains, project context |
| **RAG module** | ChromaDB | Unstructured, documentary knowledge — OWASP guidelines, CWE descriptions, CVSS explanations, remediation references, regulatory text |

The knowledge graph is the live memory of the engagement. The RAG is the static expertise library. Both agents use both layers but in different proportions — the Tester Agent leans on the graph, the Client Agent leans on both equally to produce consequence narratives grounded in both live data and verified standards.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM Orchestration | LangGraph (ReAct loop) |
| Backend API | FastAPI |
| Knowledge Graph | Neo4j |
| Vector Store | ChromaDB |
| VMS Platform | DefectDojo |
| MCP Integration | Model Context Protocol |
| Frontend | React |
| Database | PostgreSQL |
| Deployment | Docker Compose |

---

## Project structure

```
The project /
├── agents/
│   ├── tester_agent.py        # Tester Agent — LangGraph ReAct loop
│   └── client_agent.py        # Client Agent — Security Mirror logic
├── mcp/
│   └── server.py              # MCP Server — DefectDojo bridge
├── graph/
│   ├── builder.py             # Knowledge graph ingestion and enrichment
│   └── queries.py             # Graph traversal queries
├── rag/
│   ├── ingest.py              # OWASP / CWE / CVSS document ingestion
│   └── retriever.py           # RAG retrieval logic
├── api/
│   └── main.py                # FastAPI backend
├── frontend/
│   ├── tester/                # Tester workspace (split-screen)
│   └── client/                # Security Mirror dashboard
├── db/
│   └── models.py              # PostgreSQL session and profile models
├── docker-compose.yml
└── README.md
```

---

## Getting started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- A running DefectDojo instance (or use the provided Docker setup)
- Neo4j (included in Docker Compose)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourname/The project .git
cd The project 

# Copy environment variables
cp .env.example .env

# Start all services
docker-compose up --build
```

### Environment variables

```env
DEFECTDOJO_URL=http://localhost:8080
DEFECTDOJO_API_KEY=your_api_key
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
OPENAI_API_KEY=your_llm_key
POSTGRES_URL=postgresql://user:password@localhost/The project 
```

---

## Development sprints

| Sprint | Focus | Status |
|---|---|---|
| Sprint 1 — Analysis | Existing solutions study, technology benchmark, requirements | Done |
| Sprint 2 — Setup | DefectDojo Docker deployment, MCP Server, project structure | In progress |
| Sprint 3 — Tester Agent | ReAct loop, CRUD via natural language, knowledge graph builder | To do |
| Sprint 4 — Client Agent | Security Mirror dashboard, RAG integration, business context onboarding | To do |
| Sprint 5 — Integration | Auth, routing, end-to-end testing, UI finalization | To do |
| Sprint 6 — Finalization | Final testing, bug fixing, report and defense | To do |

---

## Authors

Mohamed Farouk Ben Haj Amor — ESPRIT, 2026