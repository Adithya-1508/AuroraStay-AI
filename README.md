# 🏨 AuroraStay AI: Enterprise AI-Driven Guest Experience & Booking Platform

AuroraStay AI is an enterprise-grade hospitality operations and guest experience platform. It leverages **LangGraph multi-agent workflows**, **Retrieval-Augmented Generation (RAG)**, and domain-driven design principles to deliver a seamless, automated reservation and guest assistance portal.

---

## 🏗️ System Architecture

AuroraStay AI is built on a clean, layered architecture separating core business domains, workflow orchestration, database persistence, and cognitive AI services:

```mermaid
graph TD
    %% Client Interfaces
    API_Gateway[FastAPI API Gateway] -->|HTTP Requests| API_Routes[Route Controllers]
    Chat_Gateway[FastAPI Chat Gateway] -->|Chat Payloads| Assistant_Agent[Reservation Assistant Agent]

    %% Workflows & Agents
    subgraph Workflows [Agentic Workflows Layer]
        Assistant_Agent -->|State Machine Orchestration| LangGraph[LangGraph State Machine]
        LangGraph -->|Tool Executor Nodes| Tools[Agent Tool Definitions]
    end

    %% Services & Business Logic
    subgraph Business_Domain [Business & Domain Services Layer]
        Tools -->|Query & Mutate| Reservation_Service[Reservation Service]
        Tools -->|Query Availability| Availability_Service[Availability Service]
        Reservation_Service -->|Upgrade Check| Allocation_Engine[Loyalty Allocation Engine]
        Reservation_Service -->|Price Computations| Pricing_Engine[Stay Pricing Engine]
        Reservation_Service -->|Email/SMS Logs| Notification_Service[Notification Service]
        Reservation_Service -->|Audit Logs| History_Service[State History Service]
    end

    %% Knowledge Platform (RAG)
    subgraph Knowledge_Platform [Knowledge Platform RAG]
        Assistant_Agent -->|RAG Context Fetch| Retrieval_Engine[Semantic Retriever Engine]
        Retrieval_Engine -->|Fetch Documents| Qdrant[Qdrant Vector DB]
        Retrieval_Engine -->|Rerank Matches| Nvidia_Reranker[NVIDIA NIM QA Reranker]
        Nvidia_Reranker -->|Refine Response Context| Assistant_Agent
    end

    %% Database & Persistence
    subgraph Database_Persistence [Persistence & Data Layer]
        Reservation_Service -->|Unit of Work| UOW[Postgres/SQLite Unit of Work]
        UOW -->|Commit Transaction| DB[(PostgreSQL / SQLite Database)]
    end
```

---

## 🌟 Core Features

### 1. 🤖 LangGraph Multi-Agent Orchestrator
- **State Machine Routing**: Manages customer conversation nodes, active memory checkpoints, and interrupts using a state graph pattern.
- **AI Tool Executor**: Equips the assistant with schemas for availability search, stay pricing calculation, booking reservations, reservation modifications/cancellations, and upgrade eligibility checks.

### 2. 🛏️ Intelligent Booking & Allocation Engines
- **Priority Upgrades**: Automatically upgrades loyalty program members (Platinum/Gold) to higher vacant room categories (e.g., Deluxe or Suites) if the requested room category is fully occupied.
- **Availability Calendar Engine**: Suggests shifted stay dates and alternative vacant room categories if standard criteria are unavailable.
- **Pricing Calculation Engine**: Dynamically calculates reservation costs factoring in base category price, promo codes, and loyalty tier discounts.

### 3. 📚 Knowledge Platform (RAG)
- **Multi-Format Parsers**: Built-in support for PDF, DOCX, Markdown, HTML, CSV, and JSON ingestion.
- **NVIDIA NIM Reranking**: Utilizes `nvidia/rerank-qa-mistral-4b` models with character-overlap fallback algorithms for contextual precision.
- **Rigorous Citations**: Formats all conversational assistant answers with clickable source provenance tags mapping to document names and specific page/header metrics.

---

## 🛠️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Async API routing & dependency injection)
- **Orchestration**: [LangGraph](https://www.langchain.com/langgraph) / [LangChain](https://www.langchain.com/) (Multi-agent workflows)
- **ORM & Database**: [SQLAlchemy 2.0 Async](https://www.sqlalchemy.org/) & [Alembic](https://alembic.sqlalchemy.org/) (Migrations)
- **Vector DB**: [Qdrant](https://qdrant.tech/) (Semantic search storage)
- **Reranker AI**: [NVIDIA NIM API](https://build.nvidia.com/nvidia/rerank-qa-mistral-4b)
- **Code Quality**: [Ruff](https://github.com/astral-sh/ruff) (Linter/Formatter), [Mypy](https://mypy-lang.org/) (Static Type Check)
- **Testing**: [Pytest](https://docs.pytest.org/) (Isolated unit tests and coverage metrics)

---

## 🚀 Getting Started

### 1. Bootstrap Environment Variables
Set up your configurations and secrets:
```bash
python scripts/bootstrap.py
```

### 2. Setup Virtual Environment & Dependencies
Initialize environment using `uv` or `pip`:
```bash
uv venv
uv pip install -e .[dev,test,ml]
```

### 3. Launch Docker Services
Spins up PostgreSQL database, Qdrant vector database, and mock integrations:
```bash
docker compose up -d
```

### 4. Run Code Quality & Tests
Execute all static validations and unit tests:
```bash
# Run code formatter, linter, and type checker
python scripts/lint_all.py

# Run unit tests with package coverage
python -m pytest --cov=business/reservation business/reservation/tests/
```
All verification tests pass with **96% code coverage** for core reservation business logic modules.
