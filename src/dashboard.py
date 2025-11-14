import streamlit as st
import pandas as pd
import numpy as np

# from fase1_area_insumos import ...
# from fase1_meteorologia import ...
# from fase2_previsao_insumos import ...
# from fase3_iot_esp32 import ...
# from fase3_bomba_agua import ...
# from fase4_ml_model import ...
# from fase6_yolo_vision import ...
# from fase5_cloud_alerts import send_alert

st.set_page_config(
    page_title="Sistema Agrícola Inteligente",
    layout="wide",
)

st.title("🌾 Sistema de Gestão Agrícola Inteligente — Fase 7")


def create_mock_dataframe(rows=10):
    return pd.DataFrame({
        "Tempo": pd.date_range("2024-01-01", periods=rows),
        "Umidade (%)": np.random.randint(20, 90, rows),
        "Temperatura (°C)": np.random.randint(18, 40, rows),
        "pH": np.random.uniform(5.5, 7.5, rows).round(2),
    })


def banner(text, color="#025928"):
    st.markdown(
        f"""
        <div style='padding:12px; background-color:{color}; color:white; border-radius:8px;'>
            <b>{text}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.title("📌 Navegação")
aba = st.sidebar.radio(
    "Selecione a etapa:",
    [
        "🏠 Visão Geral",
        "🌱 Fase 1 — Plantio e Insumos",
        "📦 Fase 2 — Previsão de Insumos",
        "💧 Fase 3 — Sensores e Irrigação",
        "🤖 Fase 4 — Modelo Preditivo",
        "🪲 Fase 6 — Visão Computacional",
        "📨 Alertas AWS",
    ]
)



if aba == "🏠 Visão Geral":
    banner("Dashboard Geral da Fazenda — Status Atual", "#0f4c75")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Temperatura Atual", "28°C", "+2°C vs ontem")
    col2.metric("💧 Umidade do Solo", "41%", "-7% vs ontem")
    col3.metric("🌥️ Última Análise Climática", "Normal")

    st.subheader("📊 Histórico de Leituras dos Sensores")
    df = create_mock_dataframe(30)
    st.line_chart(df[["Umidade (%)", "Temperatura (°C)"]])



elif aba == "🌱 Fase 1 — Plantio e Insumos":
    banner("Fase 1 — Cálculo de Área, Insumos e Meteorologia", "#588157")

    st.subheader("🌾 Cadastro de Área e Plantio")
    if st.button("Cadastrar nova cultura"):
        st.info("Função real será integrada depois (fase1_area_insumos.py).")

    st.subheader("📦 Manejo de Insumos (Entradas e Saídas)")
    if st.button("Registrar movimentação de insumos"):
        st.info("Função real será integrada depois.")

    st.subheader("🌦️ Consultar API Meteorológica")
    if st.button("Buscar dados de meteorologia"):
        st.success("Meteorologia consultada (simulação).")

    st.write(create_mock_dataframe(7))



elif aba == "📦 Fase 2 — Previsão de Insumos":
    banner("Fase 2 — Regressão Linear para Prever Demanda de Insumos", "#52796f")

    if st.button("Calcular previsão de demanda futura"):
        st.success("Modelo de regressão linear executado (mock).")

    st.write("📈 Previsões mockadas:")
    st.line_chart(pd.DataFrame({
        "Dias": range(30),
        "Demanda Prevista": np.random.randint(10, 100, 30)
    }))



elif aba == "💧 Fase 3 — Sensores e Irrigação":
    banner("Fase 3 — IoT com ESP32 (Sensores + Irrigação)", "#40916c")

    if st.button("Sincronizar sensores ESP32"):
        st.info("Dados do ESP32 coletados (simulação).")

    if st.button("Ativar bomba de irrigação"):
        st.warning("Bomba ativada (simulação).")

    st.subheader("📉 Leituras recentes do ESP32")
    df = create_mock_dataframe(15)
    st.dataframe(df)



elif aba == "🤖 Fase 4 — Modelo Preditivo":
    banner("Fase 4 — Random Forest para Previsões de Manejo", "#1d3557")

    if st.button("Rodar modelo preditivo agora"):
        st.success("Random Forest executado (mock).")

    st.subheader("📈 Previsão de necessidade de irrigação")
    chart_df = pd.DataFrame({
        "Dia": range(10),
        "Necessidade (%)": np.random.randint(10, 100, 10)
    })
    st.bar_chart(chart_df)



elif aba == "🪲 Fase 6 — Visão Computacional":
    banner("Fase 6 — YOLO para detecção de pragas/doenças", "#6a040f")

    uploaded = st.file_uploader("Envie uma imagem da plantação", type=["jpg", "png"])

    if uploaded and st.button("Analisar imagem"):
        st.image(uploaded, caption="Imagem recebida (mock).")
        st.error("⚠️ Praga detectada: Lagarta — 82% de confiança (simulação).")



elif aba == "📨 Alertas AWS":
    banner("Integração AWS SNS — Envio de Alertas Automáticos", "#14213d")

    subject = st.text_input("Assunto do alerta")
    message = st.text_area("Mensagem do alerta")

    if st.button("Enviar alerta"):
        st.success("Alerta enviado via SNS (simulação).")

