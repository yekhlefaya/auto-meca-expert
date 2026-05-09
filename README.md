# 🚗 Auto-Méca Expert — Système Multi-Agent pour Véhicules Hybrides

> **Projet 2 – Module Systèmes Multi-Agents**  
> Assistant de support technique pour mécaniciens spécialisés hybrides

---

## 📋 Description

**Auto-Méca Expert** est un agent intelligent de support technique destiné aux mécaniciens professionnels travaillant sur des véhicules hybrides (Toyota Prius, Honda Hybrid, etc.).

Le système implémente trois fonctionnalités avancées :
1. **Sélection dynamique de modèle** selon la complexité de la requête
2. **Mémoire de session** pour suivre les étapes de réparation effectuées
3. **RAG (Retrieval-Augmented Generation)** pour consulter les manuels techniques constructeurs

---

## 🏗️ Architecture

```
auto_meca_expert/
│
├── agent.py              ← Cœur du système : agent, outils, middleware RAG
├── app.py                ← Interface Streamlit
├── requirements.txt      ← Dépendances Python
├── .env                  ← Clé API OpenAI
│
└── manuals/              ← Base de connaissances RAG
    ├── manuel_toyota_prius.txt
    └── manuel_honda_hybrid.txt
```

---

## ⚙️ Composants Clés

### 1. Sélection Dynamique de Modèle (`dynamic_model_selection`)

Le middleware analyse chaque requête utilisateur et choisit automatiquement le modèle adapté :

| Mots-clés détectés | Modèle sélectionné | Usage |
|---|---|---|
| `diagnostic`, `panne`, `erreur code`, `moteur`, `défaillance`, `code p`… | `gpt-4-turbo` | Analyse complexe, raisonnement multi-étapes |
| Requêtes simples (stock, info générale) | `gpt-3.5-turbo` | Réponses rapides, économie de tokens |

```python
@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    user_text = request.messages[-1].content.lower()
    is_complex = any(kw in user_text for kw in COMPLEX_KEYWORDS)
    if is_complex:
        return handler(request.override(model=llm_advanced))  # gpt-4-turbo
    return handler(request.override(model=llm_base))          # gpt-3.5-turbo
```

### 2. Mémoire de Session (`InMemorySaver`)

LangGraph's `InMemorySaver` maintient l'historique complet de la conversation par `thread_id`. L'agent se souvient des étapes de réparation déjà effectuées et évite de répéter les diagnostics.

```python
checkpointer = InMemorySaver()
agent = create_agent(
    ...,
    checkpointer=checkpointer,
)
# Chaque invocation utilise le même thread_id pour continuer la conversation
response = agent.invoke(
    input={"messages": [HumanMessage(user_input)]},
    config={"configurable": {"thread_id": "session_001"}},
)
```

### 3. Outil RAG : `search_technical_manuals`

- Les manuels constructeurs (`.txt` ou `.pdf`) sont découpés en chunks de 1000 caractères
- Chaque chunk est vectorisé avec `OpenAIEmbeddings` et stocké dans `FAISS`
- À chaque requête, les 4 chunks les plus pertinents sont récupérés et injectés dans le contexte

```python
@tool
def search_technical_manuals(issue: str) -> str:
    """Recherche dans les manuels de réparation constructeur."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(issue)
    return "\n\n".join([doc.page_content for doc in docs])
```

### 4. Outil Stock : `check_spare_parts`

- Vérifie la disponibilité d'une pièce dans l'inventaire simulé
- Retourne : statut (en stock / rupture), quantité, prix, référence constructeur
- Recherche exacte + recherche partielle par mots-clés

---

## 🚀 Installation et Lancement

### Prérequis
- Python 3.10+
- Clé API OpenAI

### Installation

```bash
# 1. Cloner / télécharger le projet
cd auto_meca_expert

# 2. Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la clé API
# Créer un fichier .env :
echo "OPENAI_API_KEY=votre_clé_ici" > .env
```

### Lancer l'interface web

```bash
streamlit run app.py
```

L'interface sera disponible sur : **http://localhost:8501**

### Lancer en mode console (optionnel)

```bash
python agent.py
```

---

## 💬 Exemples d'utilisation

### Diagnostic de panne (→ gpt-4-turbo activé)
```
Mécanicien: Mon client a une Toyota Prius 2020, le code erreur P0A0F s'affiche.
            La voiture démarre difficilement. Que faire ?
```

### Vérification de stock (→ gpt-3.5-turbo)
```
Mécanicien: Est-ce que vous avez des bougies NGK en stock pour la Prius ?
```

### Suivi de réparation (mémoire active)
```
Mécanicien: [message 1] J'ai un problème de panne moteur sur une Honda Civic Hybrid
Mécanicien: [message 2] J'ai vérifié la batterie IMA, elle est à 155V
Mécanicien: [message 3] Quelles sont les prochaines étapes ?  ← L'agent se souvient des étapes précédentes
```

### Ajout de manuels personnalisés
Via la sidebar de l'interface : uploader un PDF ou TXT → cliquer "Indexer les documents"

---

## 🔧 Personnalisation

### Ajouter des mots-clés pour gpt-4-turbo
Dans `agent.py`, modifier la liste :
```python
COMPLEX_KEYWORDS = ["diagnostic", "panne", "erreur code", "moteur", ...]
```

### Ajouter des pièces à l'inventaire
Dans `agent.py`, section `SPARE_PARTS_INVENTORY` :
```python
"nom de la pièce": {"qty": 5, "price": 150.00, "ref": "REF-001"},
```

### Ajouter des manuels techniques
Déposer des fichiers `.txt` ou `.pdf` dans le dossier `manuals/` et relancer l'application.

---

## 📦 Dépendances Principales

| Package | Version | Usage |
|---|---|---|
| `langchain` | ≥0.3 | Framework agents |
| `langchain-openai` | ≥0.3 | Modèles OpenAI |
| `langgraph` | ≥0.2 | Mémoire `InMemorySaver` |
| `faiss-cpu` | ≥1.7 | Index vectoriel RAG |
| `streamlit` | ≥1.40 | Interface utilisateur |
| `pypdf2` | ≥3.0 | Lecture PDF |
| `python-dotenv` | ≥1.0 | Variables d'environnement |

---

## 🔒 Sécurité

- La clé API est stockée dans `.env` et jamais exposée dans le code
- **Ne pas committer le fichier `.env`** dans Git (ajouter `.env` au `.gitignore`)
- Pour les interventions haute tension, l'agent rappelle systématiquement les procédures de mise en sécurité

---

## 👥 Auteurs

Projet réalisé dans le cadre du **Module Systèmes Multi-Agents**  
Basé sur LangChain + LangGraph + OpenAI GPT
