import os
import sys

from src.fase1.cap1_python.src.calculations import calculate_input_quantity

CURRENT_FILE = os.path.abspath(__file__)
FINAL_DIR = os.path.dirname(CURRENT_FILE)
SRC_DIR = os.path.dirname(FINAL_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import numpy as np
import math

from src.final.services.aws_alert_service import send_alert

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
    html = '''
        <div style="padding:12px; background-color:{color}; color:white; border-radius:8px;">
            <b>{text}</b>
        </div>
    '''.format(color=color, text=text)
    st.markdown(html, unsafe_allow_html=True)


def compute_area(shape: str, width=None, length=None, side=None, radius=None) -> float:
    """
    Replica a lógica de cálculo de área da Fase 1,
    mas usando parâmetros ao invés de input() no terminal.
    """
    shape = shape.lower()
    if shape in ["retângulo", "retangulo"]:
        if width is None or length is None:
            return 0.0
        return width * length
    elif shape == "quadrado":
        if side is None:
            return 0.0
        return side ** 2
    elif shape in ["círculo", "circulo"]:
        if radius is None:
            return 0.0
        return math.pi * (radius ** 2)
    return 0.0


# Estado global para culturas da Fase 1
if "crops" not in st.session_state:
    st.session_state.crops = []


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


# =========================
# VISÃO GERAL
# =========================
if aba == "🏠 Visão Geral":
    banner("Dashboard Geral da Fazenda — Status Atual", "#0f4c75")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌡️ Temperatura Atual", "28°C", "+2°C vs ontem")
    col2.metric("💧 Umidade do Solo", "41%", "-7% vs ontem")
    col3.metric("🌥️ Última Análise Climática", "Normal")

    st.subheader("📊 Histórico de Leituras dos Sensores")
    df = create_mock_dataframe(30)
    st.line_chart(df[["Umidade (%)", "Temperatura (°C)"]])


# =========================
# FASE 1 – PLANTIO E INSUMOS
# =========================
elif aba == "🌱 Fase 1 — Plantio e Insumos":
    banner("Fase 1 — Cálculo de Área, Insumos e Meteorologia", "#588157")

    st.subheader("🌾 Cadastro de Área e Plantio")

    # Formulário para cadastrar nova cultura
    with st.form("form_nova_cultura", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            crop_name = st.text_input("Nome da cultura", "")
            shape = st.selectbox(
                "Forma geométrica da área",
                ["retângulo", "quadrado", "círculo"],
            )

        with col_b:
            spacing = st.number_input(
                "Espaçamento entre linhas/sulcos (m)",
                min_value=0.1,
                value=0.5,
                step=0.1,
                format="%.2f",
            )

        st.markdown("### Dimensões da área")
        if shape in ["retângulo", "retangulo"]:
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Largura (m)", min_value=0.1, value=10.0, step=0.5)
            with col2:
                length = st.number_input("Comprimento (m)", min_value=0.1, value=20.0, step=0.5)
            side = None
            radius = None
        elif shape == "quadrado":
            side = st.number_input("Lado (m)", min_value=0.1, value=10.0, step=0.5)
            width = None
            length = None
            radius = None
        else:  # círculo
            radius = st.number_input("Raio (m)", min_value=0.1, value=5.0, step=0.5)
            width = None
            length = None
            side = None

        submitted = st.form_submit_button("➕ Cadastrar cultura")

        if submitted:
            if not crop_name.strip():
                st.warning("Informe o nome da cultura.")
            else:
                total_area = compute_area(shape, width=width, length=length, side=side, radius=radius)
                if total_area <= 0:
                    st.error("Não foi possível calcular a área. Verifique os dados.")
                else:
                    # Mesma lógica do main.py (linhas, área de sulcos, área de cultivo)
                    rows = int(total_area / spacing) if spacing > 0 else 0
                    groove_area = rows * spacing * 0.25
                    cultivation_area = total_area - groove_area

                    new_crop = {
                        "crop": crop_name,
                        "shape": shape,
                        "spacing": spacing,
                        "total_area": total_area,
                        "cultivation_area": cultivation_area,
                        "groove_area": groove_area,
                        "rows": rows,
                        "inputs": [],
                    }
                    st.session_state.crops.append(new_crop)
                    st.success(f"Cultura '{crop_name}' cadastrada com sucesso!")


    st.subheader("✏️ Atualizar Cultura Existente")

    if not st.session_state.crops:
        st.info("Nenhuma cultura cadastrada para atualizar.")
    else:
        names = [c["crop"] for c in st.session_state.crops]
        selected = st.selectbox("Selecione a cultura para atualizar:", names)

        crop = next(c for c in st.session_state.crops if c["crop"] == selected)

        with st.form("form_update_crop"):
            st.markdown("### 🔄 Atualizando dados da cultura")

            col1, col2 = st.columns(2)
            with col1:
                new_shape = st.selectbox(
                    "Forma geométrica",
                    ["retângulo", "quadrado", "círculo"],
                    index=["retângulo","quadrado","círculo"].index(crop["shape"]),
                )
            with col2:
                new_spacing = st.number_input(
                    "Espaçamento (m)",
                    value=float(crop["spacing"]),
                    min_value=0.1,
                    step=0.1,
                    format="%.2f"
                )

            st.markdown("### 🧮 Novas dimensões")

            if new_shape == "retângulo":
                colA, colB = st.columns(2)
                width = colA.number_input(
                    "Largura (m)",
                    value=crop.get("width", 10.0),
                    min_value=0.1,
                    step=0.5
                )
                length = colB.number_input(
                    "Comprimento (m)",
                    value=crop.get("length", 20.0),
                    min_value=0.1,
                    step=0.5
                )
                side = None
                radius = None

            elif new_shape == "quadrado":
                side = st.number_input(
                    "Lado (m)",
                    value=crop.get("side", 10.0),
                    min_value=0.1,
                    step=0.5
                )
                width = None
                length = None
                radius = None

            else:
                radius = st.number_input(
                    "Raio (m)",
                    value=crop.get("radius", 5.0),
                    min_value=0.1,
                    step=0.5
                )
                width = None
                length = None
                side = None

            update_button = st.form_submit_button("💾 Salvar alterações")

            if update_button:
                # 1. Recalcular área exatamente como na Fase 1
                total_area = compute_area(new_shape, width, length, side, radius)
                rows = int(total_area / new_spacing)
                groove_area = rows * new_spacing * 0.25
                cultivation_area = total_area - groove_area

                # 2. Atualizar cultura
                crop["shape"] = new_shape
                crop["spacing"] = new_spacing
                crop["total_area"] = total_area
                crop["cultivation_area"] = cultivation_area
                crop["groove_area"] = groove_area
                crop["rows"] = rows

                # salvar dimensões
                crop["width"] = width
                crop["length"] = length
                crop["side"] = side
                crop["radius"] = radius

                # 3. Recalcular TODOS os insumos dessa cultura
                for ins in crop["inputs"]:
                    ins["total_quantity"] = calculate_input_quantity(
                        cultivation_area,
                        ins["quantity_per_area"],
                        rows,
                    )

                st.success(f"Cultura '{selected}' atualizada com sucesso!")
                st.experimental_rerun()



    st.subheader("📦 Cadastro de Insumos por Cultura")

    if not st.session_state.crops:
        st.info("Cadastre uma cultura primeiro para adicionar insumos.")
    else:
        crop_names = [c["crop"] for c in st.session_state.crops]
        with st.form("form_novo_insumo", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                selected_crop_name = st.selectbox("Selecione a cultura", crop_names)
            with col2:
                input_name = st.text_input("Nome do insumo/produto")

            col3, col4 = st.columns(2)
            with col3:
                unit = st.text_input("Unidade do insumo (ex: litros, kg)", "kg")
            with col4:
                quantity_per_area = st.number_input(
                    "Quantidade por área (unidade/m²)",
                    min_value=0.0,
                    value=1.0,
                    step=0.1,
                    format="%.2f",
                )

            submit_input = st.form_submit_button("➕ Adicionar insumo")

            if submit_input:
                if not input_name.strip():
                    st.warning("Informe o nome do insumo.")
                else:
                    crop = next(c for c in st.session_state.crops if c["crop"] == selected_crop_name)
                    total_quantity = calculate_input_quantity(
                        crop["cultivation_area"],
                        quantity_per_area,
                        crop["rows"],
                    )
                    new_input = {
                        "input_name": input_name,
                        "unit": unit,
                        "quantity_per_area": quantity_per_area,
                        "total_quantity": total_quantity,
                    }
                    crop["inputs"].append(new_input)
                    st.success(
                        f"Insumo '{input_name}' adicionado à cultura '{selected_crop_name}'. "
                        f"Quantidade total necessária: {total_quantity:.2f} {unit}"
                    )

    st.subheader("📊 Culturas cadastradas e insumos calculados")

    if not st.session_state.crops:
        st.info("Nenhuma cultura cadastrada ainda.")
    else:
        for idx, crop in enumerate(st.session_state.crops):
            with st.expander(f"Cultura {idx + 1}: {crop['crop'].capitalize()}", expanded=False):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Área total (m²)", f"{crop['total_area']:.2f}")
                col_b.metric("Área de cultivo útil (m²)", f"{crop['cultivation_area']:.2f}")
                col_c.metric("Nº de linhas/sulcos", crop["rows"])

                st.write(f"• Forma geométrica: **{crop['shape']}**")
                st.write(f"• Espaçamento entre linhas: **{crop['spacing']} m**")
                st.write(f"• Área de sulcos/carreador: **{crop['groove_area']:.2f} m²**")

                if crop["inputs"]:
                    st.markdown("#### Insumos cadastrados")
                    insumos_df = pd.DataFrame(crop["inputs"])
                    insumos_df.rename(
                        columns={
                            "input_name": "Insumo",
                            "unit": "Unidade",
                            "quantity_per_area": "Qtd/área (unidade/m²)",
                            "total_quantity": "Qtd total necessária",
                        },
                        inplace=True,
                    )
                    st.dataframe(insumos_df)
                else:
                    st.info("Nenhum insumo cadastrado para esta cultura.")

                delete_button = st.button(
                    f"🗑️ Excluir cultura '{crop['crop']}'",
                    key=f"delete_crop_{idx}",
                )
                if delete_button:
                    st.session_state.crops.pop(idx)
                    st.success(f"Cultura '{crop['crop']}' removida com sucesso.")
                    st.experimental_rerun()


# =========================
# FASE 2 – MOCK (a integrar depois)
# =========================
elif aba == "📦 Fase 2 — Previsão de Insumos":
    banner("Fase 2 — Regressão Linear para Prever Demanda de Insumos", "#52796f")

    if st.button("Calcular previsão de demanda futura"):
        st.success("Modelo de regressão linear executado (mock).")

    st.write("📈 Previsões mockadas:")
    st.line_chart(pd.DataFrame({
        "Dias": range(30),
        "Demanda Prevista": np.random.randint(10, 100, 30)
    }))


# =========================
# FASE 3 – MOCK (sensores + irrigação)
# =========================
elif aba == "💧 Fase 3 — Sensores e Irrigação":
    banner("Fase 3 — IoT com ESP32 (Sensores + Irrigação)", "#40916c")

    if st.button("Sincronizar sensores ESP32"):
        st.info("Dados do ESP32 coletados (simulação).")

    if st.button("Ativar bomba de irrigação"):
        st.warning("Bomba ativada (simulação).")

    st.subheader("📉 Leituras recentes do ESP32")
    df = create_mock_dataframe(15)
    st.dataframe(df)


# =========================
# FASE 4 – MOCK (modelo preditivo)
# =========================
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


# =========================
# FASE 6 – MOCK (visão computacional)
# =========================
elif aba == "🪲 Fase 6 — Visão Computacional":
    banner("Fase 6 — YOLO para detecção de pragas/doenças", "#6a040f")

    uploaded = st.file_uploader("Envie uma imagem da plantação", type=["jpg", "png"])

    if uploaded and st.button("Analisar imagem"):
        st.image(uploaded, caption="Imagem recebida (mock).")
        st.error("⚠️ Praga detectada: Lagarta — 82% de confiança (simulação).")


# =========================
# ALERTAS AWS (SNS)
# =========================
elif aba == "📨 Alertas AWS":
    banner("Integração AWS SNS — Envio de Alertas Automáticos", "#14213d")

    subject = st.text_input("Assunto do alerta", "Alerta da Fazenda Inteligente")
    message = st.text_area("Mensagem do alerta")

    if st.button("Enviar alerta"):
        result = send_alert(message, subject)
        if result["ok"]:
            st.success(f"Alerta enviado! MessageId: {result['message_id']}")
        else:
            st.error(f"Erro ao enviar: {result['error']}")
