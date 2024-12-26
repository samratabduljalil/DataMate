# Local RAG System: Chat with Your PDFs (Using Ollama, LaMDA, and LangChain)

Welcome to your personal PDF interaction powerhouse! This project lets you upload PDF documents and engage in conversational search using powerful language models (LLMs). It leverages Ollama and LaMDA (LLM3) for advanced natural language processing (NLP), and uses LangChain as the framework.

## Key Features

*   **Local Deployment:** Runs entirely on your local system, ensuring privacy and data security.
*   **Conversational Search:** Interact with your PDFs in a natural, chat-like manner. Ask questions and receive relevant answers.
*   **LLM Integration:** Uses cutting-edge LLMs like Ollama and LaMDA (LLM3) for accurate text comprehension.
*   **Embedding and Database (ChromaDB):** Uses `nomic-embed-text` for embeddings and ChromaDB for efficient document storage and retrieval.

## Getting Started

### Prerequisites

*   **Python:** Ensure you have Python 3.x installed (`python --version`).
*   **Git:** You'll need Git to clone the repository. Download it from [https://git-scm.com/](https://git-scm.com/).
*   **Ollama:** Install and set up Ollama. See the Ollama documentation for instructions.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone <your_repository_url>.git
    cd <repository_name>
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    This will install the necessary Python libraries, including `langchain`, `chromadb`, `nomic-embed-text`, and others.

### Configuration (Ollama)

Before starting the application, ensure Ollama is running and accessible. If your Ollama server is running on a non-default host/port (other than `127.0.0.1:11434`), you *must* set the `OLLAMA_HOST` environment variable:

```bash
export OLLAMA_HOST=127.0.0.1:12345 # Example: If Ollama runs on port 12345