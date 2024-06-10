import re
from datasets import Dataset


def parse_question_and_options(text: str):
    # Extract the question part
    question_match = re.search(r"Question:\s*(.*)\s*Options:", text, re.DOTALL)
    question = question_match.group(1).strip() if question_match else ""

    # Extract the options part
    options_match = re.search(r"Options:\s*(.*)\s*Answer:", text, re.DOTALL)
    options_text = options_match.group(1).strip() if options_match else ""

    # Split options into a list and clean them
    options = [opt.strip() for opt in options_text.split("\n") if opt.strip()]

    return question, options


def process_docs(dataset: Dataset):
    def _helper(doc):
        question = doc["question"]
        answer_letter = doc["answer"]
        question, options = parse_question_and_options(question)
        answer = options[ord(answer_letter) - ord("A")]

        doc = {
            "question": question,
            "options": "\n".join(options),
            "choices": options,
            "answer": answer,
        }
        print(doc)
        return doc

    return dataset.map(_helper)
