
# Cet outil simule une base de données relationnelle contenant des informations
# sur les clients et les produits d'une PME. Il permet à l'agent de répondre à
# des questions du type : «Quel est le solde du compte de Marie Dupont ?» ou «Combien coûte le produit X ?»

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')


def _get_connection():
    return sqlite3.connect(DB_PATH)


def rechercher_client(query: str) -> str:
    """Recherche un client par nom ou par identifiant."""
    query = query.strip()
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, nom, solde_compte, type_compte FROM clients WHERE id = ?',
        (query.upper(),)
    )
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            'SELECT id, nom, solde_compte, type_compte FROM clients WHERE LOWER(nom) LIKE ?',
            (f'%{query.lower()}%',)
        )
        row = cursor.fetchone()

    conn.close()

    if row:
        cid, nom, solde, type_compte = row
        return f"Client : {nom} | Solde : {solde:.2f} € | Type de compte : {type_compte}"
    return f"Aucun client trouvé pour : '{query}'"


def rechercher_produit(query: str) -> str:
    """Recherche un produit par nom ou identifiant. Retourne prix HT, TVA, prix TTC, stock."""
    query = query.strip()
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, nom, prix_ht, stock FROM produits WHERE id = ?',
        (query.upper(),)
    )
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            'SELECT id, nom, prix_ht, stock FROM produits WHERE LOWER(nom) LIKE ?',
            (f'%{query.lower()}%',)
        )
        row = cursor.fetchone()

    conn.close()

    if row:
        pid, nom, prix_ht, stock = row
        tva = prix_ht * 0.20
        prix_ttc = prix_ht + tva
        return (f"Produit : {nom} | Prix HT : {prix_ht:.2f} € "
                f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {stock}")
    return f"Aucun produit trouvé pour : '{query}'"


def lister_tous_les_clients(query: str = "") -> str:
    """Retourne la liste complète de tous les clients."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nom, type_compte, solde_compte FROM clients')
    rows = cursor.fetchall()
    conn.close()

    result = "Liste des clients :\n"
    for cid, nom, type_compte, solde in rows:
        result += f"  {cid} : {nom} | {type_compte} | Solde : {solde:.2f} €\n"
    return result
