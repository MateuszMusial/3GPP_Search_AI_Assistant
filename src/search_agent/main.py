#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from dotenv import load_dotenv

from .document_processors.pdf_processor import PDFProcessor
from .query_executor import QueryExecutor
from .cli_parser import parse_cli_args


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    load_dotenv()

    query_executor = QueryExecutor(file_processor=PDFProcessor())
    args = parse_cli_args()

    result = query_executor.execute_query(args.ie)
    print("Query Result:", result)

if __name__ == "__main__":
    main()