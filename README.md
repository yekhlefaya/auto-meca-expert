# Auto-Méca Expert — AI Diagnostic Assistant for Hybrid Vehicles

> Intelligent multi-agent support system for hybrid vehicle diagnostics and technical assistance.

---

## Overview

**Auto-Méca Expert** is an AI-powered technical assistant designed for mechanics working on hybrid vehicles such as Toyota Prius and Honda Hybrid models.

The system combines modern AI engineering concepts including:

- Dynamic LLM routing based on query complexity
- Conversational memory with LangGraph
- Retrieval-Augmented Generation (RAG)
- Technical manual retrieval using FAISS vector search
- Streamlit conversational interface

---

## Key Features

### 🔹 Dynamic Model Selection
The system automatically routes requests to the most suitable model:

- **GPT-4 Turbo** → complex diagnostics and multi-step reasoning
- **GPT-3.5 Turbo** → lightweight and faster requests

### 🔹 Conversational Memory
Using `LangGraph InMemorySaver`, the assistant maintains repair history during the session and tracks previous diagnostic steps.

### 🔹 RAG-based Technical Search
Technical manuals are indexed with `OpenAIEmbeddings` and stored in `FAISS` to retrieve relevant repair procedures and documentation.

### 🔹 Spare Parts Assistant
Integrated inventory tool for checking:
- availability
- quantity
- price
- manufacturer reference

---

## Project Structure

```bash
auto_meca_expert/
│
├── agent.py
├── app.py
├── requirements.txt
├── manuals/
│   ├── manuel_toyota_prius.txt
│   └── manuel_honda_hybrid.txt
```

---

## Technologies

| Category | Technologies |
|---|---|
| AI / LLMs | OpenAI GPT-4, GPT-3.5 |
| Frameworks | LangChain, LangGraph |
| RAG | FAISS, OpenAI Embeddings |
| Interface | Streamlit |
| Backend | Python |
| Document Processing | PyPDF2 |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YekhlefAya/auto-meca-expert.git
cd auto-meca-expert
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate environment

#### Windows
```bash
.venv\Scripts\activate
```

#### Linux / MacOS
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

---

## Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```bash
http://localhost:8501
```

---

## Example Queries

### Complex Diagnostic Request
```text
My Toyota Prius displays error code P0A0F and struggles to start.
What diagnostic steps should I follow?
```

### Spare Parts Verification
```text
Do you have NGK spark plugs available for Toyota Prius?
```

### Multi-step Repair Session
```text
I checked the IMA battery and measured 155V.
What should I verify next?
```

---

## Main Dependencies

| Package | Purpose |
|---|---|
| LangChain | Agent orchestration |
| LangGraph | Conversational memory |
| FAISS | Vector database |
| Streamlit | Web interface |
| OpenAI | LLM integration |
| PyPDF2 | PDF processing |

---

## Security

- API keys are stored using environment variables
- Sensitive credentials are excluded from version control
- Technical recommendations include hybrid vehicle safety precautions

---

## License

This project is licensed under the MIT License.

---

## Author

Developed by **Aya Yekhlef**  
AI & Data Engineering Student