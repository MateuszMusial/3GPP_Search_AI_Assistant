# 📂 3GPP Documentation Directory (/data)

This folder is dedicated to storing the raw 3GPP specification files used as the primary knowledge base for the LLM Agent.

## 📥 Purpose
Any PDF file placed in this directory will be automatically processed, chunked, and indexed into the vector database to enable Retrieval-Augmented Generation (RAG).

## 🛠 File Requirements
To ensure the highest quality of model responses, please follow these guidelines:

* **Format:** Only `.pdf` files are supported.
* **Source:** It is recommended to download documents directly from the official [3gpp.org](https://www.3gpp.org/ftp/Specs/archive/) portal.
* **Language:** Documents must be in English (3GPP standard).

## 🏷 Naming Convention
While the system can read any filename, it is best practice to keep the original 3GPP naming format to assist in metadata extraction (Spec number, Version, Release):
* Example: `23501-g30.pdf` (TS 23.501, Release 16)
* Example: `38331-h20.pdf` (TS 38.331, Release 17)
