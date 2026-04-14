# Projet Agent LangChain - TP Automatisation

Projet d'agent intelligent utilisant LangChain pour effectuer des tâches financières, de calculs et de recherche d'informations.

## Fonctionnalités Implémentées

### A1 - Base de données SQLite (2 pts)
- Migration des données vers SQLite
- Script d'initialisation `init_db.py`
- Requêtes SQL pour clients et produits

### A2 - Cours boursiers réels avec yfinance (2 pts)
- Récupération des cours en temps réel
- Variation du jour et volume
- Support actions et cryptomonnaies

### A3 - Recherche web avec TavilySearch (2 pts)
- Recherche web en temps réel
- Actualités financières
- Informations sur entreprises

### B1 - Calcul de portefeuille boursier (2 pts)
- Calcul de valeur totale
- Variation globale du jour
- Format: `SYMBOLE:QUANTITE|SYMBOLE:QUANTITE`

### B2 - PythonREPLTool (4 pts)
- Exécution de code Python
- Calculs complexes
- Traitement de données

### C1 - Interface Streamlit (2 pts)
- Interface web interactive
- Historique des conversations
- Liste des outils disponibles

### C2 - Mémoire conversationnelle (2 pts)
- ConversationBufferMemory
- Contexte conservé entre questions
- Agent create_openai_tools_agent

### D1 - API REST (4 pts)
- FastAPI
- Endpoint POST /api/agent/query
- Réponses JSON structurées

## Installation

### 1. Cloner le projet

```bash
cd projet-automatisation
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Créer un fichier `.env` à partir de `.env.example`:

```bash
cp .env.example .env
```

Éditer `.env` et remplir avec vos clés API:
- `OPENAI_API_KEY`: obligatoire - obtenir sur https://platform.openai.com
- `TAVILY_API_KEY`: optionnel - obtenir sur https://tavily.com

### 4. Initialiser la base de données

```bash
python init_db.py
```

## Utilisation

### Mode Console (original)

```bash
python main.py
```

Choisissez un scénario numéroté ou tapez 'quit' pour quitter.

### Mode Streamlit (interface web)

```bash
streamlit run app.py
```

Ouvrir le navigateur à l'adresse indiquée (généralement http://localhost:8501).

### Mode API REST

```bash
python api.py
```

L'API démarre sur http://localhost:8000

Tester avec curl:

```bash
curl -X POST http://localhost:8000/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quel est le cours d Apple ?"}'
```

Documentation interactive: http://localhost:8000/docs

## Structure du Projet

```
projet-automatisation/
├── main.py                 # Point d'entrée console
├── app.py                  # Interface Streamlit
├── api.py                  # API REST FastAPI
├── agent.py                # Configuration de l'agent
├── init_db.py              # Initialisation base de données
├── database.db             # Base de données SQLite (généré)
├── requirements.txt        # Dépendances Python
├── .env.example            # Template configuration
├── tools/
│   ├── database.py         # Outils base de données
│   ├── finance.py          # Cours boursiers (yfinance)
│   ├── portefeuille.py     # Calcul portefeuille
│   ├── calculs.py          # Calculs financiers
│   ├── api_publique.py     # API devises
│   ├── text.py             # Traitement texte
│   └── recommandation.py   # Recommandations produits
└── README.md               # Ce fichier
```

## Exemples de Questions

### Finance
- "Quel est le cours actuel d'Apple (AAPL) ?"
- "Calcule mon portefeuille: AAPL:10|MSFT:5|TSLA:3"
- "Quelle est la variation du Bitcoin aujourd'hui ?"

### Base de données
- "Quelles sont les infos du client Marie Dupont ?"
- "Quel est le prix du produit P001 ?"

### Calculs
- "Calcule la TVA sur 100 EUR à 20%"
- "Mensualité pour un prêt de 200000 EUR sur 20 ans à 4%"

### Recherche web (si TAVILY_API_KEY configuré)
- "Actualités Apple aujourd'hui"
- "Résultats trimestriels Tesla"

### Mémoire conversationnelle
```
Q1: "Donne-moi les infos du client Sophie Bernard"
Q2: "Quel produit lui recommandes-tu ?"
Q3: "Peut-elle se le permettre ?"
```

## Notes de Sécurité

- **PythonREPLTool**: Exécute du code arbitraire. Ne jamais utiliser en production sans sandbox.
- **API**: Pas d'authentification implémentée. À ajouter pour production.
- **Clés API**: Ne jamais commiter le fichier `.env` dans Git.

## Technologies Utilisées

- LangChain (agents, outils, mémoire)
- OpenAI GPT-4
- yfinance (données boursières)
- Tavily (recherche web)
- SQLite (base de données)
- Streamlit (interface web)
- FastAPI (API REST)

## Auteur

Esteban PAGIS (dans le cadre du projet tp_stagiaire.pdf)