#!/usr/bin/env python3
# Interface web Streamlit pour l'agent LangChain

import streamlit as st
from dotenv import load_dotenv
from agent import creer_agent, tools

load_dotenv()

st.set_page_config(
    page_title="Agent LangChain",
    page_icon=":robot:",
    layout="wide"
)

st.title("Agent LangChain Intelligent")
st.markdown("Posez vos questions financières, techniques ou de données.")

# Sidebar avec infos sur les outils
with st.sidebar:
    st.header("Outils disponibles")
    st.markdown("L'agent dispose de " + str(len(tools)) + " outils :")
    for tool in tools:
        st.markdown(f"- **{tool.name}**")

    st.divider()

    if st.button("Réinitialiser la conversation"):
        st.session_state.messages = []
        st.session_state.agent = creer_agent()
        st.rerun()

# Initialisation de l'agent et de l'historique
if 'agent' not in st.session_state:
    with st.spinner("Initialisation de l'agent..."):
        st.session_state.agent = creer_agent()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Votre question..."):
    # Affichage de la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                response = st.session_state.agent.invoke(
                    {"input": prompt},
                    config={"configurable": {"session_id": "streamlit-session"}}
                )
                answer = response['output']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"Erreur : {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
