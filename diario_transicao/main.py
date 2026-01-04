import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd

ARQUIVO = "dados.json"


# ---------- UTIL ----------
def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def classificar_disforia(nivel):
    if nivel <= 2:
        return "Muito baixa"
    elif nivel <= 4:
        return "Baixa"
    elif nivel <= 6:
        return "Moderada"
    elif nivel <= 8:
        return "Alta"
    else:
        return "Muito alta"


# ---------- APP ----------
st.set_page_config(page_title="Diário de Transição", page_icon="🏳️‍⚧️")

st.title("🏳️‍⚧️ Diário de Transição")

dados = carregar_dados()

# ---------- CICLO ----------
st.header("🔁 Ciclo Hormonal")

ciclo = st.number_input(
    "Escolha o ciclo (em dias)",
    min_value=0,
    max_value=90,
    value=dados.get("ciclo", 21),
    step=1
)

if st.button("Salvar ciclo"):
    dados["ciclo"] = ciclo
    salvar_dados(dados)
    st.success(f"Ciclo salvo: {ciclo} dias")

# ---------- HORMÔNIO ----------
st.header("💉 Aplicação de Hormônio")

data_aplicacao = st.date_input("Data da última aplicação")

if st.button("Calcular próxima aplicação"):
    proxima = data_aplicacao + timedelta(days=ciclo)

    dados.setdefault("hormonio", [])
    dados["hormonio"].append({
        "data": data_aplicacao.strftime("%d/%m/%Y"),
        "ciclo": ciclo,
        "proxima": proxima.strftime("%d/%m/%Y")
    })

    salvar_dados(dados)
    st.success(f"Próxima aplicação: {proxima.strftime('%d/%m/%Y')}")

# ---------- DISFORIA ----------
st.header("💙 Disforia")

nivel = st.slider("Nível de disforia (0 a 10)", 0, 10, 5)

if st.button("Registrar disforia"):
    descricao = classificar_disforia(nivel)

    dados.setdefault("disforia", [])
    dados["disforia"].append({
        "data": datetime.now().strftime("%d/%m/%Y"),
        "nivel": nivel,
        "descricao": descricao
    })

    salvar_dados(dados)
    st.success(f"Disforia registrada: {nivel} ({descricao})")

# ---------- GRÁFICO ----------
import matplotlib.pyplot as plt

st.header("📈 Evolução da Disforia")

registros = dados.get("disforia", [])

if registros:
    df = pd.DataFrame(registros)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

    fig, ax = plt.subplots()
    ax.plot(df["data"], df["nivel"], marker="o")

    ax.set_ylim(0, 10)
    ax.set_xlabel("Data")
    ax.set_ylabel("Nível de Disforia")
    ax.set_title("Disforia ao longo do tempo")
    ax.grid(True)

    st.pyplot(fig)
else:
    st.info("Ainda não há registros de disforia.")


