import sys
import os
import subprocess
import tempfile
import time

import memory


def commit_to_memory_and_answer_question_about_page_text(url, text, question):
    text_length = len(text)
    now = time.time()
    print_to_err(f"Committing to memory: answers to question \"{question}\" about the webpage {url}")

    print_to_err(f"Page text length: {text_length} characters")
    answers = []
    chunks = list(split_text(text))
    scroll_ratio = 1 / len(chunks)
    print_to_err(f"Page text broken into {len(chunks)} chunks")

    # TODO: Check memory for chunks ie. use it as cache rather than refetch every time
    for i, chunk in enumerate(chunks):
        print_to_err(f"Adding chunk {i + 1} / {len(chunks)} to memory")

        content_chunk_memory = f"URL: {url}\n" f"Content chunk #{i + 1}:\n{chunk}"

        memory.create_memory(
            content_chunk_memory,
            metadata={
                "analysed_at": now,
                "uri": url,
                "chunk_number": i+1,
                "chunk_text": text
            }
        )

        print_to_err(f"Answering question of chunk {i + 1} / {len(chunks)}")

        answer = ask_ai_question_about_text(question, chunk)
        answers.append(answer)

        print_to_err(f"Adding chunk {i + 1} answer to memory")

        answer_from_chunk_memory = f"URL: {url}\nQuestion: {question}\nAnswer from chunk #{i + 1}:\n{answer}"

        print_to_err(answer_from_chunk_memory)

        memory.create_memory(
            answer_from_chunk_memory,
            metadata={
                "analysed_at": now,
                "uri": url,
                "chunk_number": i+1,
                "chunk_text": text,
                "question": question,
                "answer": answer_from_chunk_memory
            }
        )

    print_to_err(f"Asked question over {len(chunks)} chunks.")


    print_to_err(f"Asking question of cumulative answers.")
    # TODO: guard somehow against this being too large
    all_answers = "\n".join(answers)
    answer_derived_from_all_chunk_answers = ask_ai_question_about_text(question, all_answers)

    answer_derived_from_all_chunk_answers_memory = f"URL: {url}\nQuestion: {question}\nAnswer derived from all chunks' answers:\n{answer_derived_from_all_chunk_answers}"

    print_to_err(answer_derived_from_all_chunk_answers_memory)

    memory.create_memory(
        answer_derived_from_all_chunk_answers_memory,
        metadata={
            "analysed_at": now,
            "uri": url,
            "chunk_number": i+1,
            "chunk_text": text,
            "question": question,
            "answer": answer_from_chunk_memory
        }
    )

    return answer_derived_from_all_chunk_answers

def ask_ai_question_about_text(question, text):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(text.encode("utf-8"))
        temp_file_path = os.path.abspath(temp_file.name)
        temp_file.close()
        answer = subprocess.check_output(f"tools/ask_ai_question_about_text_file \"{question}\" \"{temp_file_path}\"", shell=True, encoding="utf8")
    return answer

def print_to_err(text):
    print(text, file=sys.stderr)

def split_text(text, max_length=8192):
    paragraphs = text.split("\n")
    current_length = 0
    current_chunk = []

    for index, paragraph in enumerate(paragraphs):
        if len(paragraph) > max_length:
            paragraphs.insert(index+1, paragraph[max_length:])
            paragraph = paragraph[:max_length]

        if current_length + len(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk = [paragraph]
            current_length = len(paragraph) + 1

    if current_chunk:
        yield "\n".join(current_chunk)

