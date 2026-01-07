# NLP SaveBuddy

SaveBuddy is an intelligent NLP microservice designed for fintech applications. It acts as an interpretation layer, converting natural language user commands (e.g., "Save $50 for my trip next week") into structured transaction data.

## Features

- **Intent Classification**: Distinguishes between Personal Savings and Group Contributions.
- **Entity Extraction**: Extracts Amount, Currency, Frequency, Dates, and Target Groups/Goals.
- **Context Awareness**: Enriches prompts with user context (existing groups, goals) for accurate matching.
- **Microservice Architecture**: Built with FastAPI, Docker-ready, and stateless.

## Documentation

For a detailed deep-dive into the NLP capabilities and logic, see [SaveBuddy Feature Docs](docs/SAVEBUDDY.md).

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional, for containerized run)

### Local Setup

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd nlp-savebuddy
    ```

2.  **Create and activate virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Copy `.env.example` to `.env` and configure accordingly.
    ```bash
    cp .env.example .env
    ```

5.  **Run the application**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Docker Setup

You can run the entire service using the provided Makefile or Docker Compose.

```bash
# Build and Run
make build

# Run tests inside container
make test

# View logs
make logs
```

## Running Tests

To run the test suite locally:

```bash
pytest tests/
```

## Tech Stack

- **Framework**: FastAPI
- **NLP Models**: HuggingFace Transformers (QA & Sentence Embeddings)
- **Containerization**: Docker
