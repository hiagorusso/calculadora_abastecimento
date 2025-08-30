from supabase import create_client
import streamlit as st
import toml

def iniciar_supabase():
    """Inicializa o cliente Supabase usando os secrets do Streamlit Cloud."""
    try:
        # Usando st.secrets para obter as credenciais diretamente
        url = st.secrets["SUPABASE"]["SUPABASE_URL"]
        key = st.secrets["SUPABASE"]["SUPABASE_KEY"]

        if not url or not key:
            raise ValueError("SUPABASE_URL ou SUPABASE_KEY estão vazios ou inválidos.")

        client = create_client(url, key)
        print("Cliente Supabase inicializado com sucesso!")
        return client
    except Exception as e:
        print(f"Erro ao inicializar o cliente Supabase: {e}")
        return None
