from langchain_classic.tools import Tool
from tools.database import lister_tous_les_clients, rechercher_client, rechercher_produit
from tools.recommandation import recommander_produits
from tools.text import formater_rapport, extraire_mots_cles, convertir_majuscules_minuscules, resumer_texte
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.api_publique import convertir_devise, obtenir_taux_du_jour
from tools.calculs import calculer_tva, calculer_interets_composes, calculer_marge, calculer_mensualite_pret
from tools.portefeuille import calculer_portefeuille
from tools.portfolio_db import (
    analyser_risques_portefeuille,
    obtenir_positions_client,
    analyser_secteurs_portefeuille,
    obtenir_historique_symbole
)
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
import os

tools = [
    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),

    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),

    Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),

    Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours d\'une crypto. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),

    Tool(name='calculer_tva', func=calculer_tva,
         description='Calcule TVA et prix TTC. Entrée : une chaîne "prix_ht,taux" ex "100,20".'),

    Tool(name='calculer_interets', func=calculer_interets_composes,
         description='Intérêts composés. Entrée : une chaîne "capital,taux_annuel,années" ex "10000,5,3".'),

    Tool(name='calculer_marge', func=calculer_marge,
         description='Calcule la marge commerciale. '
                     'Entrée : chaîne "prix_vente,cout_achat" ex "1200,899".'),

    Tool(name='calculer_mensualite', func=calculer_mensualite_pret,
         description='Mensualité prêt. Entrée : une chaîne "capital,taux_annuel,mois" ex "200000,3.5,240".'),

    Tool(name='convertir_devise', func=convertir_devise,
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'Entrée : une chaîne "montant,DEV_SOURCE,DEV_CIBLE" ex "100,USD,EUR".'),

    Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),

    Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),

    Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),

    Tool(name='recommander_produits', func=recommander_produits,
         description='Recommandations produits selon budget, catégorie et type de compte. '
                     'Entrée : chaîne "budget,categorie,type_compte" ex "300,Informatique,Premium". '
                     'Catégories : Informatique, Mobilier, Audio, Toutes. '
                     'Types : Standard, Premium, VIP.'),

    Tool(name='calculer_portefeuille', func=calculer_portefeuille,
         description='Calcule la valeur totale d\'un portefeuille d\'actions en temps réel. '
                     'Entrée : chaîne "SYMBOLE:QUANTITE|SYMBOLE:QUANTITE" ex "AAPL:10|MSFT:5|TSLA:3".'),

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
         description='Historique des 7 derniers jours d\'un symbole. '
                     'Entrée : symbole ex "AAPL".'),
]

if os.getenv('TAVILY_API_KEY'):
    tavily_search = TavilySearchResults(max_results=3)
    tavily_search.name = 'recherche_web'
    tavily_search.description = (
        'Recherche web en temps réel pour questions d\'actualité, '
        'informations sur entreprises, news financières. '
        'Entrée : question ou mots-clés.'
    )
    tools.append(tavily_search)

# ATTENTION: PythonREPLTool exécute du code arbitraire
# Ne pas utiliser en production sans sandbox
python_repl = PythonREPLTool()
python_repl.name = 'executer_python'
python_repl.description = (
    'Exécute du code Python pour calculs complexes. '
    'Entrée : code Python valide.'
)
tools.append(python_repl)


def creer_agent():
    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
    from langchain_classic import hub
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.runnables.history import RunnableWithMessageHistory
    import os

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    prompt = hub.pull("hwchase17/openai-tools-agent")
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        handle_parsing_errors=True
    )

    memory = InMemoryChatMessageHistory()
    agent_with_memory = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_memory


def interroger_agent(agent, question: str, session_id: str = "default"):
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}}
    )
    print(f"\nRéponse finale : {result['output']}")
    return result
