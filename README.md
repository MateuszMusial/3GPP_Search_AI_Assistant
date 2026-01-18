# 3GPP Search Agent

A Retrieval-Augmented Generation (RAG) tool for querying 3GPP Technical Specifications (specifically TS 38.331, TS 36.331, and TS 24.501). This tool leverages LLM model and FAISS vector search to provide accurate, context-aware answers to protocol-related questions.

## Features

- **RAG Pipeline:** Efficiently retrieves relevant document chunks and generates answers using LLM Model.
- **Vector Search:** Uses FAISS for fast similarity search on embedded 3GPP documents.


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

2.  **Install dependencies:**
    Using `uv`:
    ```bash
    uv sync
    ```
    Or using `pip`:
    ```bash
    pip install .
    ```

3.  **Environment Configuration:**
    Create a `.env` file in the root directory:
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    MODEL_NAME=gemini-2.5-pro
    EMBEDDING_MODEL_NAME=models/embedding-001
    ```

4.  **Prepare Data:**
    Place your 3GPP PDF documents (e.g., `ts_124501v171600p.pdf`) in the `data/` directory.


### Running Tests

```bash
uv run pytest
```