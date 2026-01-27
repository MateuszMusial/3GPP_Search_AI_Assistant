# 3GPP Search Agent

A Retrieval-Augmented Generation (RAG) tool for querying 3GPP Technical Specifications (specifically TS 38.331, TS 36.331, and TS 24.501). This tool leverages LLM model and FAISS vector search to provide accurate, context-aware answers to protocol-related questions.

## Features

- **RAG Pipeline:** Efficiently retrieves relevant document chunks and generates answers using LLM Model.
- **Vector Search:** Uses FAISS for fast similarity search on embedded 3GPP documents.

## Project Structure

The core application code resides in the `src/search_agent/` directory, following a standard Python src-layout.

## Prerequisites

- Python 3.13+
- `uv` package manager (recommended) or `pip`
- Google Cloud API Key (for Gemini models)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd 3gpp_search_agent
    ```

2.  **Install dependencies and project in editable mode:**
    Using `uv`:
    ```bash
    uv sync
    ```
    This command will install all required dependencies and the `3gpp-search-agent` package itself in editable mode, making it importable.

3.  **Environment Configuration:**
    Create a `.env` file in the root directory and set your Google API Key:
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    ```

4.  **Prepare Data:**
    Place your 3GPP PDF documents (e.g., `ts_124501v171600p.pdf`) in the `data/` directory.

## Usage

### Running the Application

To run the main application logic, which will process documents (and create the FAISS index if it doesn't exist) and execute a sample query:

```bash
uv run python -m search_agent.main
```

### Running Tests

To execute the test suite:

```bash
uv run pytest
```