# GitHub Repository Assistant

> **Understand, explore, and chat with any GitHub repository using AI-powered repository search.**

GitHub Repository Assistant is an AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to interact with a GitHub repository using natural language.

Instead of manually searching through multiple files, users can provide a GitHub repository URL and ask questions such as:

* What does this project do?
* How does a particular function work?
* Which technologies are used?
* Explain this file.
* Where is a specific feature implemented?
* How does the application handle authentication?
* Explain the overall project architecture.

The assistant retrieves relevant code and documentation from the repository and uses an LLM to generate contextual answers.

---

## Features

* 🔗 **GitHub Repository Integration**

  * Enter any accessible GitHub repository URL.
  * Fetch repository files using the GitHub API.

* 📂 **Automatic Repository Processing**

  * Recursively discovers files inside the repository.
  * Reads supported source-code and documentation files.

* ✂️ **Intelligent Text Chunking**

  * Splits large files into smaller chunks for efficient retrieval.

* 🧠 **Hugging Face Embeddings**

  * Converts repository content into vector embeddings.

* 🗄️ **ChromaDB Vector Store**

  * Stores embeddings for semantic similarity search.
  * Enables efficient retrieval of relevant repository content.

* 🔎 **Semantic Repository Search**

  * Retrieves code and documentation based on the meaning of the user's question rather than simple keyword matching.

* 🤖 **LLM-Powered Answers**

  * Uses an instruction-tuned language model through the Hugging Face Router.

* 💬 **Natural-Language Chat**

  * Ask questions about the repository conversationally.

* ⚡ **Streamlit Interface**

  * Provides an interactive web interface for repository analysis and chat.

* 💡 **Context-Aware Responses**

  * Answers are generated using retrieved repository context instead of relying only on the model's general knowledge.

---

## How It Works

The application follows a typical **RAG pipeline**:

```text
                GitHub Repository URL
                         │
                         ▼
                  GitHub API
                         │
                         ▼
                  Repository Files
                         │
                         ▼
                 Document Processing
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
             Hugging Face Embeddings
                         │
                         ▼
                    ChromaDB
                         │
                         ▼
                Semantic Retrieval
                         │
                  User Question
                         │
                         ▼
               Relevant Code Chunks
                         │
                         ▼
                  LLM + Context
                         │
                         ▼
                   AI Response
```

### 1. Repository Input

The user provides a GitHub repository URL through the application.

Example:

```text
https://github.com/username/repository
```

### 2. Repository Loading

The GitHub API is used to access the repository and retrieve its files.

The application recursively explores the repository structure and collects relevant files.

### 3. Document Processing

Repository files are converted into documents that can be processed by the RAG pipeline.

Large files are divided into smaller chunks using a text splitter.

### 4. Embedding Generation

Each document chunk is converted into a numerical vector using **Hugging Face embeddings**.

These vectors represent the semantic meaning of the repository content.

### 5. Vector Storage

The generated embeddings are stored in **ChromaDB**.

This allows the application to perform similarity searches when the user asks a question.

### 6. Question Processing

When the user asks a question, the application searches the vector database for the most relevant repository chunks.

### 7. Context + LLM

The retrieved chunks are provided to the language model along with the user's question.

The LLM then generates an answer based on the retrieved repository context.

This approach helps the assistant answer questions specifically about the selected repository.

---

## Tech Stack

| Technology                | Purpose                            |
| ------------------------- | ---------------------------------- |
| **Python**                | Core programming language          |
| **Streamlit**             | Web application interface          |
| **LangChain**             | RAG pipeline and LLM orchestration |
| **PyGithub**              | GitHub API integration             |
| **Hugging Face**          | Embeddings and LLM access          |
| **ChromaDB**              | Vector database                    |
| **Qwen 2.5 72B Instruct** | Language model                     |
| **python-dotenv**         | Environment variable management    |

---

## Project Structure

```text
GitHub-Repository-Assistant/
│
├── app.py
│
├── src/
│   ├── github_loader.py
│   ├── document_processor.py
│   ├── vector_store.py
│   └── rag_chain.py
│
├── chroma_db/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### Main Components

#### `app.py`

The main Streamlit application.

It handles:

* User interface
* Repository URL input
* Repository analysis
* Chat interface
* Session state
* RAG pipeline execution

#### `github_loader.py`

Responsible for communicating with GitHub.

Main responsibilities include:

* Connecting to GitHub
* Getting repository information
* Recursively retrieving repository files
* Reading file contents

#### `document_processor.py`

Handles repository content preparation.

Responsibilities:

* Creating LangChain documents
* Splitting documents into chunks
* Preparing content for embedding

#### `vector_store.py`

Handles ChromaDB.

Responsibilities:

* Creating the vector store
* Adding document embeddings
* Creating the retriever
* Performing semantic similarity search

#### `rag_chain.py`

Contains the RAG logic.

Responsibilities:

* Creating the prompt
* Retrieving relevant context
* Passing context to the LLM
* Generating the final response

---

## Models

### Embedding Model

The project uses **Hugging Face embeddings** to convert repository documents into vector representations.

This enables semantic search across the codebase.

### Language Model

The project uses:

```text
Qwen/Qwen2.5-72B-Instruct
```

through the Hugging Face Router using LangChain's `ChatOpenAI` interface.

The model receives:

```text
User Question
      +
Retrieved Repository Context
      ↓
Language Model
      ↓
Final Answer
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShravaniKale18/GitHub-Repository-Assistant.git
```

```bash
cd GitHub-Repository-Assistant
```

### 2. Create a Virtual Environment

Using Python:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
GITHUB_TOKEN=your_github_token
HF_TOKEN=your_huggingface_token
```

### GitHub Token

The GitHub token is used to authenticate GitHub API requests and helps avoid unauthenticated API rate limits.

### Hugging Face Token

The Hugging Face token is used to access the embedding/model services.

> **Never commit your `.env` file or API tokens to GitHub.**

Add this to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
chroma_db/
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

Then:

1. Enter a GitHub repository URL.
2. Click **Analyze Repository**.
3. Wait for the repository to be processed.
4. Ask questions about the repository.
5. Receive AI-generated answers based on the repository content.

---

## Example Questions

After analyzing a repository, you can ask:

```text
What does this project do?
```

```text
Explain the project architecture.
```

```text
Which technologies are used in this project?
```

```text
Explain the main function in app.py.
```

```text
How does authentication work?
```

```text
Where is the database connection created?
```

```text
Explain how the API works in this project.
```

```text
What is the purpose of the vector_store.py file?
```

```text
How does the application retrieve relevant documents?
```

---

## RAG Architecture

The project uses the following RAG components:

### Retriever

The retriever searches the ChromaDB vector store and returns repository chunks that are semantically similar to the user's question.

### Context Creation

The retrieved documents are combined into a context that is passed to the LLM.

### Prompt

The model receives both the repository context and the user's question.

Conceptually:

```text
Context:
<relevant repository content>

Question:
<user question>

Answer:
```

This helps keep the generated response grounded in the repository.

---

## Why RAG?

A normal LLM does not automatically know the contents of a private or recently changed GitHub repository.

RAG solves this problem by:

1. Loading the repository.
2. Converting repository content into embeddings.
3. Storing those embeddings in a vector database.
4. Retrieving relevant content for each question.
5. Giving that content to the LLM.
6. Generating an answer using the retrieved information.

This makes the assistant useful for **repository-specific code understanding**.

---

## Important Considerations

### GitHub API Rate Limits

GitHub imposes API rate limits. Using an authenticated GitHub token provides a higher API limit than unauthenticated requests.

### Repository Size

Very large repositories may require significant time and memory to:

* Download files
* Generate embeddings
* Store vectors
* Perform retrieval

### Supported Files

The application is primarily designed for source code and documentation. Binary files and unsupported formats may be skipped.

### API Keys

Never expose GitHub or Hugging Face tokens in:

* Source code
* GitHub repositories
* Screenshots
* Public documentation

---

## Future Improvements

Potential improvements for the project include:

* [ ] Support multiple repository branches
* [ ] Improve repository file filtering
* [ ] Add file and folder navigation
* [ ] Display retrieved source files
* [ ] Add source citations to answers
* [ ] Improve conversation memory
* [ ] Add repository-specific vector-store isolation
* [ ] Add support for private repositories
* [ ] Add repository statistics and visualization
* [ ] Improve code-aware chunking
* [ ] Add GitHub commit and history analysis
* [ ] Support multiple programming languages
* [ ] Add authentication for application users
* [ ] Deploy the application with a production backend/frontend architecture

---

## Learning Concepts Demonstrated

This project combines several important concepts in modern AI application development:

* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)
* Vector embeddings
* Vector databases
* Semantic search
* Prompt engineering
* LangChain
* GitHub API integration
* Natural language interfaces
* Streamlit application development
* Environment and API-key management

---

## Project Workflow

```text
User
 │
 │ GitHub Repository URL
 ▼
Streamlit Application
 │
 ▼
GitHub API
 │
 ▼
Repository Loader
 │
 ▼
Document Processor
 │
 ▼
Text Splitter
 │
 ▼
Hugging Face Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Retriever
 │
 ▼
Relevant Repository Context
 │
 ▼
Qwen 2.5 72B Instruct
 │
 ▼
AI-generated Answer
```

---

## Use Cases

GitHub Repository Assistant can be useful for:

* 👨‍💻 Understanding unfamiliar codebases
* 📚 Learning from open-source projects
* 🔍 Finding specific implementations
* 🐛 Debugging and understanding code
* 🏗️ Exploring project architecture
* 🎓 Academic/project demonstrations
* 📝 Understanding documentation
* 🚀 Getting started with a new repository

---

## Author

**Shravani Kale**

B.Tech IT Student

GitHub: [ShravaniKale18](https://github.com/ShravaniKale18)

---

## License

This project is intended for educational and learning purposes.
