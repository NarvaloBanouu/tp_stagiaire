#!/bin/bash
# Script de lancement rapide

echo "========================================="
echo "AGENT LANGCHAIN - MENU DE LANCEMENT"
echo "========================================="
echo ""
echo "1. Mode Console (original)"
echo "2. Mode Streamlit (interface web)"
echo "3. Mode API REST (serveur)"
echo "4. Test mémoire conversationnelle"
echo "5. Initialiser/réinitialiser la base de données"
echo ""
read -p "Votre choix (1-5): " choice

case $choice in
  1)
    echo "Lancement du mode console..."
    python3 main.py
    ;;
  2)
    echo "Lancement de Streamlit..."
    echo "Ouvrez votre navigateur à http://localhost:8501"
    streamlit run app.py
    ;;
  3)
    echo "Lancement de l'API REST..."
    echo "API disponible à http://localhost:8000"
    echo "Documentation: http://localhost:8000/docs"
    python3 api.py
    ;;
  4)
    echo "Lancement du test de mémoire..."
    python3 test_memoire.py
    ;;
  5)
    echo "Initialisation de la base de données..."
    python3 init_db.py
    ;;
  *)
    echo "Choix invalide"
    exit 1
    ;;
esac
