#!/usr/bin/env python3
# Script d'initialisation de la base de données SQLite

import sqlite3
import os

DB_PATH = 'database.db'

# Données initiales
CLIENTS_DATA = [
    ("C001", "Marie Dupont", "marie.dupont@email.fr", "Paris", 15420.50, "Premium", "2021-03-15", 8750.00),
    ("C002", "Jean Martin", "jean.martin@email.fr", "Lyon", 3200.00, "Standard", "2022-01-10", 1200.00),
    ("C003", "Sophie Bernard", "sophie.bernard@email.fr", "Marseille", 28900.00, "VIP", "2020-06-20", 15600.00),
    ("C004", "Lucas Petit", "lucas.petit@email.fr", "Toulouse", 750.00, "Standard", "2023-02-05", 300.00)
]

PRODUITS_DATA = [
    ("P001", "Ordinateur portable Pro", 899.00, 45),
    ("P002", "Souris ergonomique", 49.90, 120),
    ("P003", "Bureau réglable", 350.00, 18),
    ("P004", "Casque audio sans fil", 129.00, 67),
    ("P005", "Écran 27 pouces 4K", 549.00, 30)
]


def init_database():
    """Crée et initialise la base de données SQLite."""
    # Supprime l'ancienne base si elle existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[OK] Ancienne base de données supprimée")

    # Connexion et création
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Création de la table clients
    cursor.execute('''
        CREATE TABLE clients (
            id TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            email TEXT,
            ville TEXT,
            solde_compte REAL NOT NULL,
            type_compte TEXT NOT NULL,
            date_inscription TEXT,
            achats_total REAL
        )
    ''')

    # Création de la table produits
    cursor.execute('''
        CREATE TABLE produits (
            id TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            prix_ht REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Insertion des données clients
    cursor.executemany(
        'INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        CLIENTS_DATA
    )

    # Insertion des données produits
    cursor.executemany(
        'INSERT INTO produits VALUES (?, ?, ?, ?)',
        PRODUITS_DATA
    )

    conn.commit()
    conn.close()

    print(f"[OK] Base de données '{DB_PATH}' créée avec succès")
    print(f"   - {len(CLIENTS_DATA)} clients insérés")
    print(f"   - {len(PRODUITS_DATA)} produits insérés")


if __name__ == "__main__":
    init_database()
