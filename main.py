#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from dotenv import load_dotenv

from rag_pipeline import start_rag_pipeline, create_model
from document_processors.pdf_processor import PDFProcessor


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    load_dotenv()
    file_processor = PDFProcessor()

    vectorstore = start_rag_pipeline(file_processor=file_processor)
    print(f"Vectorstore state: {vectorstore}")

    model = create_model()
    
    if vectorstore:
        model_response = model.invoke("hi")
        print("Model response:", model_response)


if __name__ == "__main__":
    main()