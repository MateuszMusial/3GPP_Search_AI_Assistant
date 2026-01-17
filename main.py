#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from dotenv import load_dotenv

from rag_pipeline import start_rag_pipeline, create_model


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    load_dotenv()

    vectorstore = start_rag_pipeline()
    print(f"Vectorstore state: {vectorstore}")

    model = create_model()
    
    if vectorstore:
        model_response = model.invoke("explain me faiss db in simple terms")
        print("Model response:", model_response)


if __name__ == "__main__":
    main()