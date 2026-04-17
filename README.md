# Agent LangChain — TP Automatisation

## Installation

```bash
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
```

Remplir `.env`

## Initialisation des bases de données

```bash
python3 init_db.py           # base clients/produits (database.db)
python3 init_portfolio_db.py # base portefeuille (portfolio.db)
```

## Lancement

**Script tout-en-un (recommandé)**
```bash
bash run.sh
```

---

Ou manuellement :

**Console interactive**
```bash
python3 main.py
```

**Interface web Streamlit**
```bash
streamlit run app.py
# ouvrir http://localhost:8501
```

**API REST**
```bash
python3 api.py
# API sur http://localhost:8000
# Documentation : http://localhost:8000/docs
```

Exemple d'appel API :
```bash
curl -X POST http://localhost:8000/api/agent/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quel est le cours de AAPL ?"}'
```
