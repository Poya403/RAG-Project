
# Student RAG - Academic Regulations Question Answering System

## Overview

Student RAG is a conversational question-answering system designed to help students understand undergraduate academic regulations at Shahrood University of Technology.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from official academic regulations and generate answers based on the retrieved content.

It is also designed to maintain student profiles and relevant conversation history, allowing the system to provide more context-aware and personalized responses.

## Project Objectives

- Extract text from academic regulation PDF documents.
- Retrieve relevant sections of the regulations based on student questions.
- Generate answers grounded in the retrieved documents.
- Maintain student profiles, including academic information such as major and admission year.
- Use relevant conversation history to understand follow-up questions.
- Provide source references, such as page numbers, to support generated answers.

## Planned Features

- PDF text extraction and document preprocessing.
- Text chunking and metadata management.
- Semantic search using text embeddings.
- Vector-based document retrieval.
- Integration with a Large Language Model (LLM).
- Conversation history and student profile management.
- A simple chat interface.
- Testing and evaluation of answer quality.

## Technology Stack

- Python
- PyMuPDF for PDF text extraction
- Sentence Transformers for text embeddings
- FAISS or Chroma for vector search
- SQLite for storing student profiles and conversation history
- A compatible Large Language Model (LLM)
- Streamlit for the user interface

Additional dependencies will be introduced as the project develops.

## Project Structure

```text
student-rag/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── tests/
├── requirements.txt
└── README.md
```

- `data/raw/`: Original PDF documents.
- `data/processed/`: Extracted and processed document data.
- `src/`: Application source code.
- `tests/`: Automated tests and evaluation scripts.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## Setup

### 1. Create a Virtual Environment

On Windows, open a terminal in the project directory and run:

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

### 4. Add the Academic Regulations PDF

Place the original PDF document in the following directory:

```text
data/raw/
```

Official document source:

[Shahrood University of Technology - Academic Regulations](https://shahroodut.ac.ir/fa/download.php?id=1111174984)

## Development Status

The project is currently in its initial setup stage.

The first implementation milestone is to extract text from the academic regulations PDF and verify the quality of the extracted content.

Subsequent milestones will cover document processing, retrieval, answer generation, conversational memory, and evaluation.

## Important Notes

- Answers should be grounded in the retrieved official regulations.
- The system should indicate when the available sources are insufficient to answer a question reliably.
- Student-specific information should be used only when relevant to the question.
- Retrieved answers should include source references whenever possible.

## License

This project is being developed as an undergraduate academic project.
