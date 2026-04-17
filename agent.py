from langchain_classic.tools import Tool
from langchain_core.tools import StructuredTool
from tools.database import lister_tous_les_clients, rechercher_client, rechercher_produit
from tools.recommandation import recommander_produits
from tools.text import formater_rapport, extraire_mots_cles, convertir_majuscules_minuscules, resumer_texte
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.api_publique import convertir_devise, obtenir_taux_du_jour
from tools.calculs import calculer_tva, calculer_interets_composes, calculer_marge, calculer_mensualite_pret
from tools.portfolio import (                                          # B1 + D1
    calculer_portefeuille,
    analyser_risques_portefeuille,
    obtenir_positions_client,
    analyser_secteurs_portefeuille,
    obtenir_historique_symbole
)
from langchain_community.tools.tavily_search import TavilySearchResults  # A3
from langchain_experimental.tools import PythonREPLTool                   # B2
import os


# Wrappers à signatures explicites pour StructuredTool (multi-paramètres).
# create_openai_tools_agent passe les args via OpenAI function calling (dict/list),
# ce que Tool single-input rejette. StructuredTool les accepte nativement.

def _tva(prix_ht: str, taux: str) -> str:
    return calculer_tva(f"{prix_ht},{taux}")

def _interets(capital: str, taux_annuel: str, annees: str) -> str:
    return calculer_interets_composes(f"{capital},{taux_annuel},{annees}")

def _marge(prix_vente: str, cout_achat: str) -> str:
    return calculer_marge(f"{prix_vente},{cout_achat}")

def _mensualite(capital: str, taux_annuel: str, mois: str) -> str:
    return calculer_mensualite_pret(f"{capital},{taux_annuel},{mois}")

def _devise(montant: str, devise_source: str, devise_cible: str) -> str:
    return convertir_devise(f"{montant},{devise_source},{devise_cible}")

def _recommander(budget: str, categorie: str, type_compte: str) -> str:
    return recommander_produits(f"{budget},{categorie},{type_compte}")

tools = [

     # ── Outil 1 : Base de données ─────────────────────────────────────

    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),

    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),

    # ── Outil 2 : Données financières ─────────────────────────────────

    Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),

    Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours d\'une crypto. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),

    # ── Outil 3 : Calculs financiers ──────────────────────────────────

    StructuredTool.from_function(func=_tva, name='calculer_tva',
         description='Calcule TVA et prix TTC. ex: prix_ht=100, taux=20.'),

    StructuredTool.from_function(func=_interets, name='calculer_interets',
         description='Intérêts composés. ex: capital=10000, taux_annuel=5, annees=3.'),

    StructuredTool.from_function(func=_marge, name='calculer_marge',
         description='Marge commerciale. Utiliser le prix_ht de rechercher_produit comme cout_achat. '
                     'ex: prix_vente=1200, cout_achat=899.'),

    StructuredTool.from_function(func=_mensualite, name='calculer_mensualite',
         description='Mensualité prêt. ex: capital=200000, taux_annuel=3.5, mois=240.'),

    # ── Outil 4 : API publique ────────────────────────────────────────

    StructuredTool.from_function(func=_devise, name='convertir_devise',
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'ex: montant=100, devise_source=USD, devise_cible=EUR.'),

    # ── Outil 5 : Transformation de texte ────────────────────────────

    Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),

    Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),

    Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),

    # ── Outil 6 : Recommandation ─────────────────────────────────────

    StructuredTool.from_function(func=_recommander, name='recommander_produits',
         description='Recommandations produits selon budget, catégorie et type de compte. '
                     'Catégories : Informatique, Mobilier, Audio, Toutes. '
                     'Types : Standard, Premium, VIP. '
                     'ex: budget=300, categorie=Informatique, type_compte=Premium.'),

    # ── Outil 7 (B1) : Calcul de portefeuille boursier ───────────────

    Tool(name='calculer_portefeuille', func=calculer_portefeuille,
         description='Calcule la valeur totale d\'un portefeuille d\'actions en temps réel. '
                     'Entrée : "SYMBOLE:QUANTITE|SYMBOLE:QUANTITE" ex "AAPL:10|MSFT:5|TSLA:3".'),

    # ── Outils D1 : Analyse de portefeuille (base de données) ─────────

    Tool(name='analyser_risques', func=analyser_risques_portefeuille,
         description='Analyse les actifs les plus risqués d\'un portefeuille client. '
                     'Entrée : client_id ex "C001".'),

    Tool(name='positions_client', func=obtenir_positions_client,
         description='Retourne toutes les positions d\'un client avec détails. '
                     'Entrée : client_id ex "C001".'),

    Tool(name='repartition_sectorielle', func=analyser_secteurs_portefeuille,
         description='Analyse la répartition par secteur du portefeuille. '
                     'Entrée : client_id ex "C001".'),

    Tool(name='historique_cours', func=obtenir_historique_symbole,
         description='Historique des 7 derniers jours d\'un symbole boursier. '
                     'Entrée : symbole ex "AAPL".'),

]

# ── Outil A3 : Recherche web TavilySearch (optionnel si clé présente) ─
if os.getenv('TAVILY_API_KEY'):
    tavily_search = TavilySearchResults(max_results=3)
    tavily_search.name = 'recherche_web'
    tavily_search.description = (
        'Recherche web en temps réel pour questions d\'actualité, '
        'informations sur entreprises, news financières. '
        'Entrée : question ou mots-clés.'
    )
    tools.append(tavily_search)

# ── Outil B2 : PythonREPLTool ─────────────────────────────────────────
# ATTENTION SECURITE : cet outil exécute du code arbitraire.
# Ne jamais utiliser en production sans sandbox.
python_repl = PythonREPLTool()
python_repl.name = 'executer_python'
python_repl.description = (
    'Exécute du code Python pour des calculs complexes ou traitements '
    'de données non couverts par les autres outils. '
    'Entrée : code Python valide sous forme de chaîne.'
)
tools.append(python_repl)


def creer_agent():
    """Crée et retourne un agent LangChain configuré avec mémoire conversationnelle (C2)."""
    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent  # C2 : openai-tools
    from langchain_classic import hub
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
    import os

    # Initialisation du LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,           # 0 = déterministe (résultats reproductibles)
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    # C2 : prompt compatible avec create_openai_tools_agent
    prompt = hub.pull("hwchase17/openai-tools-agent")

    # C2 : create_openai_tools_agent à la place de create_react_agent
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    # Création de l'exécuteur
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,            # Affiche le raisonnement étape par étape
        max_iterations=15,
        handle_parsing_errors=True
    )

    # C2 : mémoire conversationnelle — contexte conservé entre les questions
    memory = InMemoryChatMessageHistory()
    agent_with_memory = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_memory


def interroger_agent(agent, question: str, session_id: str = "default"):
    """Envoie une question à l'agent et affiche la réponse finale."""
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"\nRéponse finale : {result['output']}")
    return result
