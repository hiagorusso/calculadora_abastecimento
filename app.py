import streamlit as st
import pandas as pd
from datetime import datetime
from db.connection import iniciar_supabase

# 🔑 Configurações do Supabase

supabase = iniciar_supabase()

if supabase is None:
    raise RuntimeError("Cliente Supabase não foi inicializado. Verifique suas credenciais e o arquivo secrets.toml.")

# ========================
# 📌 Aba 1 - Calculadora
# ========================
def calculadora():
    st.header("⛽ Calculadora Álcool x Gasolina")

    preco_alcool = st.number_input("Preço do Álcool (R$)", min_value=0.0, format="%.2f")
    preco_gasolina = st.number_input("Preço da Gasolina (R$)", min_value=0.0, format="%.2f")

    km_alcool = st.number_input("Média km/L no Álcool", min_value=0.0, format="%.2f")
    km_gasolina = st.number_input("Média km/L na Gasolina", min_value=0.0, format="%.2f")

    if st.button("Calcular"):
        if preco_alcool > 0 and preco_gasolina > 0 and km_alcool > 0 and km_gasolina > 0:
            custo_alcool = preco_alcool / km_alcool
            custo_gasolina = preco_gasolina / km_gasolina

            st.write(f"💰 Custo por km no Álcool: R$ {custo_alcool:.2f}")
            st.write(f"💰 Custo por km na Gasolina: R$ {custo_gasolina:.2f}")

            if custo_alcool < custo_gasolina:
                st.success("✅ Vale mais a pena abastecer com **Álcool**.")
            else:
                st.success("✅ Vale mais a pena abastecer com **Gasolina**.")
        else:
            st.warning("Preencha todos os campos!")

# ========================
# 📌 Aba 2 - Registro de Abastecimentos
# ========================
def registro():
    st.header("📝 Registro de Abastecimentos")

    with st.form("registro_form"):
        data = st.date_input("Data do abastecimento", datetime.today())
        valor_abastecimento = st.number_input("Valor total abastecido (R$)", min_value=0.0, format="%.2f")
        preco_combustivel = st.number_input("Preço do combustível (R$)", min_value=0.0, format="%.2f")
        tipo_combustivel = st.selectbox("Tipo de combustível", ["Álcool", "Gasolina"])
        posto = st.text_input("Nome do posto")

        submit = st.form_submit_button("Salvar")

        if submit:
            registro = {
                "data": str(data),
                "valor_abastecimento": valor_abastecimento,
                "preco_combustivel": preco_combustivel,
                "tipo_combustivel": tipo_combustivel,
                "nome_posto": posto
            }
            supabase.table("abastecimentos").insert(registro).execute()
            st.success("✅ Abastecimento registrado com sucesso!")

    # Mostrar registros já salvos
    st.subheader("📊 Histórico de Abastecimentos")
    data = supabase.table("abastecimentos").select("*").order("data", desc=True).execute()

    if data.data:
        df = pd.DataFrame(data.data)
        st.dataframe(df)
    else:
        st.info("Nenhum abastecimento registrado ainda.")

# ========================
# 📌 Navegação entre Abas
# ========================
abas = st.tabs(["⚖️ Calculadora", "📝 Registro de Abastecimentos"])

with abas[0]:
    calculadora()

with abas[1]:
    registro()
