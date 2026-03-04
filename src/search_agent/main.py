#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from dotenv import load_dotenv

from .rag_pipeline import RAGPipeline
from .document_processors.pdf_processor import PDFProcessor
from .query_executor import QueryExecutor
from .models.google_models import GoogleModelService
from .models.openai_models import OpenAIModelService
from .cli_parser import parse_cli_args

available_models = {
    "google": ["gemini-3-pro-preview", "gemini-2.5-flash"],
    "openai": ["gpt-5-nano", "gpt-4.0-turbo-preview"]
}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    load_dotenv()
    args = parse_cli_args()
    choosen_model = args.model

    if choosen_model in available_models["google"]:
        model_service = GoogleModelService(model_name=choosen_model)
    elif choosen_model in available_models["openai"]:
        model_service = OpenAIModelService(model_name=choosen_model)

    file_processor = PDFProcessor() # PDFProcessor is the default document processor for now

    query_executor = QueryExecutor(
        file_processor=file_processor,
        llm_model=model_service,
        pipeline=RAGPipeline(file_processor=file_processor, embedding_service=model_service.create_embedding_model())
        )

    result = query_executor.execute_query(args.ie)
    print("Query Result:", result)
    
if __name__ == "__main__":
    main()
