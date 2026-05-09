"""
Auto-Méca Expert - Agent de Support Technique pour Véhicules Hybrides
"""

import os
from dotenv import load_dotenv
from typing import Optional

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

load_dotenv(override=True)

COMPLEX_KEYWORDS = ["diagnostic", "panne", "erreur code", "moteur", "défaillance",
                    "problème", "code p", "erreur", "fault", "repair", "réparation"]

def select_model(user_text: str = "") -> ChatOpenAI:
    is_complex = any(kw in user_text.lower() for kw in COMPLEX_KEYWORDS)
    if is_complex:
        print("[Modèle] 🔴 gpt-4-turbo (requête complexe)")
        return ChatOpenAI(model="gpt-4-turbo", temperature=0.0, max_tokens=2048)
    print("[Modèle] 🟢 gpt-3.5-turbo (requête simple)")
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0, max_tokens=1024)

SPARE_PARTS_INVENTORY = {
    "batterie haute tension prius": {"qty": 2, "price": 1850.00, "ref": "G9510-47170"},
    "module batterie prius": {"qty": 8, "price": 245.00, "ref": "G9510-47080"},
    "onduleur pcu prius": {"qty": 1, "price": 1200.00, "ref": "G9200-47230"},
    "convertisseur dc/dc prius": {"qty": 3, "price": 380.00, "ref": "G9370-47050"},
    "pompe frein electrique prius": {"qty": 2, "price": 560.00, "ref": "47070-47060"},
    "bougie prius ngk": {"qty": 24, "price": 18.50, "ref": "90919-01253"},
    "filtre huile toyota": {"qty": 15, "price": 8.90, "ref": "90915-YZZD2"},
    "filtre air prius": {"qty": 6, "price": 22.00, "ref": "17801-37021"},
    "batterie ima honda civic": {"qty": 1, "price": 1650.00, "ref": "1D070-RCJ-A00"},
    "module batterie honda": {"qty": 5, "price": 198.00, "ref": "1D110-RCJ-A00"},
    "convertisseur dc/dc honda": {"qty": 2, "price": 420.00, "ref": "1A820-RCJ-A01"},
    "bougie honda iridium": {"qty": 20, "price": 22.00, "ref": "98079-5514E"},
    "filtre huile honda": {"qty": 12, "price": 9.50, "ref": "15400-PLM-A01"},
    "liquide refroidissement": {"qty": 30, "price": 12.00, "ref": "GEN-LR50"},
    "liquide frein dot4": {"qty": 20, "price": 8.00, "ref": "GEN-LF04"},
}

_vector_store: Optional[FAISS] = None

def build_vector_store(manuals_dir: str = "manuals") -> Optional[FAISS]:
    all_text = ""
    manual_files = []
    if os.path.exists(manuals_dir):
        for filename in os.listdir(manuals_dir):
            if filename.endswith((".txt", ".pdf")):
                filepath = os.path.join(manuals_dir, filename)
                manual_files.append(filepath)
                with open(filepath, "r", encoding="utf-8") as f:
                    all_text += f"\n\n=== SOURCE: {filename} ===\n\n" + f.read()
    if not all_text.strip():
        print("[RAG] ⚠️  Aucun manuel trouvé.")
        return None
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(all_text)
    print(f"[RAG] ✅ {len(manual_files)} manuels → {len(chunks)} chunks")
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.from_texts(texts=chunks, embedding=embeddings)

def get_vector_store() -> Optional[FAISS]:
    global _vector_store
    if _vector_store is None:
        _vector_store = build_vector_store()
    return _vector_store

@tool
def search_technical_manuals(issue: str) -> str:
    """Outil RAG: Recherche dans les manuels de réparation constructeur pour diagnostics, codes erreurs et procédures."""
    vs = get_vector_store()
    if vs is None:
        return "⚠️ Manuels techniques non disponibles."
    docs = vs.as_retriever(search_kwargs={"k": 4}).invoke(issue)
    if not docs:
        return f"Aucune information trouvée pour: '{issue}'"
    result = f"📚 Résultats des manuels pour: '{issue}'\n\n"
    for i, doc in enumerate(docs, 1):
        result += f"--- Extrait {i} ---\n{doc.page_content}\n\n"
    return result

@tool
def check_spare_parts(part_name: str) -> str:
    """Vérifie la disponibilité d'une pièce de rechange en stock avec prix et référence."""
    key = part_name.lower().strip()
    if key in SPARE_PARTS_INVENTORY:
        p = SPARE_PARTS_INVENTORY[key]
        s = "✅ EN STOCK" if p["qty"] > 0 else "❌ RUPTURE"
        return f"🔧 {part_name.upper()}\n   {s} | {p['qty']} unité(s) | {p['price']:.2f} € | Réf: {p['ref']}"
    matches = [(k, v) for k, v in SPARE_PARTS_INVENTORY.items()
               if any(w in k for w in key.split() if len(w) > 3)]
    if matches:
        result = f"🔍 Pièces similaires pour '{part_name}':\n"
        for k, p in matches[:3]:
            result += f"  {'✅' if p['qty']>0 else '❌'} {k.title()} - {p['qty']} unité(s) - {p['price']:.2f} € - Réf: {p['ref']}\n"
        return result
    return f"❓ Pièce '{part_name}' non trouvée."

SYSTEM_PROMPT = """Tu es Auto-Méca Expert, un assistant technique spécialisé en véhicules hybrides.

Instructions:
1. Utilise search_technical_manuals pour les questions de diagnostic/réparation/codes erreurs
2. Utilise check_spare_parts avant de recommander le remplacement d'une pièce
3. Rappelle les étapes déjà effectuées dans la conversation
4. Donne des réponses structurées avec étapes numérotées
5. Mentionne les mesures de sécurité HV (haute tension) quand nécessaire
6. Réponds toujours en français"""

_agent = None
_checkpointer = None

def create_auto_meca_agent(user_text: str = ""):
    global _agent, _checkpointer
    llm = select_model(user_text)
    if _checkpointer is None:
        _checkpointer = MemorySaver()
    _agent = create_react_agent(
        model=llm,
        tools=[search_technical_manuals, check_spare_parts],
        checkpointer=_checkpointer,
        prompt=SYSTEM_PROMPT,
    )
    return _agent

def get_agent(user_text: str = ""):
    return create_auto_meca_agent(user_text)

if __name__ == "__main__":
    print("🚗  AUTO-MÉCA EXPERT\n" + "="*40)
    get_vector_store()
    thread_id = "console_001"
    while True:
        user_input = input("🔧 Mécanicien: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue
        agent = get_agent(user_input)
        response = agent.invoke(
            {"messages": [HumanMessage(user_input)]},
            config={"configurable": {"thread_id": thread_id}},
        )
        print("\n🤖", response["messages"][-1].content, "\n")
