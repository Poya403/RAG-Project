
# Student RAG - Academic Regulations Question Answering System

## Overview

Student RAG is a question-answering system designed to help students understand undergraduate academic regulations at Shahrood University of Technology.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from official academic regulations and generate accurate, context-aware answers to students' questions.

Its goal is to make accessing and understanding academic regulations easier, faster, and more convenient for students.

## Main Features

- Answering questions based on official academic regulations.
- Semantic search to retrieve relevant regulatory information.
- Generating responses using a Large Language Model (LLM).
- Providing references to the original regulatory documents.
- Supporting conversation history and student-related context.

## Technology Stack

- Python
- PyMuPDF
- Sentence Transformers
- ChromaDB
- Large Language Models (LLMs)
- SQLite
- Streamlit

## Project Structure

```text
student-rag/
├── data/
│   ├── raw/
│   ├── processed/
│   └── vector_db/
├── src/
├── tests/
├── requirements.txt
└── README.md
```

## Setup

### 1. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 2. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Academic Regulations Source

The system uses official academic regulations published by Shahrood University of Technology.

[Shahrood University of Technology - Academic Regulations](https://shahroodut.ac.ir/fa/download.php?id=1111174984)

## License

This project is being developed as an undergraduate academic project.
