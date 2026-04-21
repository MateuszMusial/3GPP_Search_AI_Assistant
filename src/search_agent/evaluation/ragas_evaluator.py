"""
This module evaluates dataset containg questions, answers and retrieved contexts.
The evaluation is based on the RAGAS metrics like Faithfulness, AnswerCorrectness or ContextRecall.
"""

import json
from dotenv import load_dotenv

from datasets import Dataset # type: ignore
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics import (
    AnswerCorrectness,
    Faithfulness,
    ContextEntityRecall,
    ContextRecall,
)

from search_agent.models.google_models import GoogleModelService


def load_dataset() -> list[dict]:
    try:
        with open("src/search_agent/evaluation/eval_data.json", encoding="utf-8") as f:
            data = json.loads(f.read())
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading dataset: {e}")
        return []  # Return an empty list to satisfy the type hint


def transform_data(data: list[dict]) -> Dataset:
    formatted = {
        "question": [item["question"] for item in data],
        "contexts": [item["contexts"] for item in data],
        "answer": [item["answer"] for item in data],
        "ground_truth": [item["ground_truth"] for item in data],
    }
    return Dataset.from_dict(formatted)


if __name__ == "__main__":
    load_dotenv()

    model_service = GoogleModelService()

    langchain_llm = model_service.create_llm_model()
    langchain_embeddings = model_service.create_embedding_model()

    ragas_llm = LangchainLLMWrapper(langchain_llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(langchain_embeddings)

    data = load_dataset()
    transformed_data = transform_data(data)

    metrics_to_use = [
        AnswerCorrectness(llm=ragas_llm, embeddings=ragas_embeddings),
        Faithfulness(llm=ragas_llm),
        ContextEntityRecall(llm=ragas_llm),
        ContextRecall(llm=ragas_llm),
    ]

    results = evaluate(dataset=transformed_data, metrics=metrics_to_use)
    df_results = results.to_pandas() # type: ignore[union-attr]

    print(f"Results: {results}")

    df_results.to_csv("ragas_results.csv", index=False)
