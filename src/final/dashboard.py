import os
import sys
from datetime import datetime
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

CURRENT_FILE = os.path.abspath(__file__)
FINAL_DIR = os.path.dirname(CURRENT_FILE)
SRC_DIR = os.path.dirname(FINAL_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.fase1.cap1_python.src.calculations import calculate_input_quantity
# ... existing imports ...
from src.fase1.cap1_python.src.calculations import calculate_input_quantity
from src.fase2.src.repositories.crop import save_crop_to_db, get_all_crops, update_crop_harvest_date
from src.fase2.src.repositories.input import save_input_to_db, get_all_inputs, get_input_by_id, \
    save_input_application_to_db, get_applications_by_crop_id, get_applications_by_input_id
from src.fase2.src.repositories.prediction import get_historical_input_data

# --- SETUP FASE 3 ---
try:
    # Adiciona o caminho da Fase 3 ao sys.path para permitir importação dos módulos internos dela
    FASE3_DIR = os.path.join(PROJECT_ROOT, "src", "fase3", "src", "python")
    if FASE3_DIR not in sys.path:
        sys.path.append(FASE3_DIR)

    from services.sensor_service import SensorRecordService
    from services.climate_service import ClimateService
    from services.component_service import ComponentService
    from services.ml_service import MLService
    from database.oracle import get_session as get_fase3_session
    
    # Inicializa serviços da Fase 3
    f3_session = get_fase3_session()
    sensor_service = SensorRecordService(f3_session)
    climate_service = ClimateService(f3_session)
    component_service = ComponentService(f3_session)
    ml_service = MLService(f3_session)
    
    PHASE3_AVAILABLE = True
except ImportError as e:
    PHASE3_AVAILABLE = False
    PHASE3_ERROR = str(e)
    print(f"Erro ao carregar Fase 3: {e}")
except Exception as e:
    PHASE3_AVAILABLE = False
    PHASE3_ERROR = str(e)
    print(f"Erro genérico ao carregar Fase 3: {e}")
# --------------------

import streamlit as st
import pandas as pd
import numpy as np
import math

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


def fase2_load_historical_df() -> pd.DataFrame:
    """
    Usa o repositório prediction da Fase 2 para buscar os dados históricos
    de aplicações de insumos e devolve um DataFrame pronto para a UI.
    """
    rows = get_historical_input_data()  # area, productivity, input_name, input_type, unit, unit_price, quantity
    if not rows:
        return pd.DataFrame()

    data = []
    for area, productivity, input_name, input_type, unit, unit_price, quantity in rows:
        data.append(
            {
                "Área (ha)": area,
                "Produtividade (t/ha)": productivity,
                "Insumo": input_name,
                "Tipo": input_type,
                "Unidade": unit,
                "Preço unitário (R$/unidade)": unit_price,
                "Quantidade aplicada": quantity,
            }
        )

    return pd.DataFrame(data)


def fase2_run_forecast(target_area: float = 10.0, target_productivity: float = 6.0) -> pd.DataFrame | None:
    """
    Adapta a lógica de forecast.py para retornar um DataFrame para a dashboard.
    Usa get_historical_input_data da Fase 2 e LinearRegression para prever demanda.

    """
    rows = get_historical_input_data()
    if not rows:
        return None

    insumo_data: dict[str, dict[str, list]] = {}

    for area, productivity, input_name, input_type, unit, unit_price, quantity in rows:
        if input_name not in insumo_data:
            insumo_data[input_name] = {
                "X": [],
                "y": [],
                "unit": unit,
                "unit_price": unit_price,
                "input_type": input_type,
            }
        insumo_data[input_name]["X"].append([area, productivity])
        insumo_data[input_name]["y"].append(quantity)

    results: list[dict] = []

    for input_name, data in insumo_data.items():
        X = np.array(data["X"])
        y = np.array(data["y"])

        if len(X) < 2:
            # Dados demais escassos para treinar – evitamos previsão sem base
            continue

        model = LinearRegression()
        model.fit(X, y)

        predicted_quantity = float(model.predict([[target_area, target_productivity]])[0])
        estimated_cost = predicted_quantity * data["unit_price"]

        total_productivity = float(sum(x[1] for x in data["X"]))
        total_quantity = float(sum(data["y"]))
        iei = total_productivity / total_quantity if total_quantity else 0.0

        if iei > 0.5:
            classificacao = "🌟 Alta eficiência"
        elif iei >= 0.3:
            classificacao = "⚖️ Eficiência média"
        else:
            classificacao = "❗ Baixa eficiência"

        total_area = float(sum(x[0] for x in data["X"]))
        avg_quantity_per_ha = total_quantity / total_area if total_area else 0.0

        results.append(
            {
                "Insumo": input_name,
                "Tipo": data["input_type"],
                "Unidade": data["unit"],
                "Preço unitário (R$/unidade)": data["unit_price"],
                "Quantidade prevista": predicted_quantity,
                "Custo estimado (R$)": estimated_cost,
                "Índice de eficiência (t/unidade)": iei,
                "Classificação de eficiência": classificacao,
                "Uso médio por hectare (unidade/ha)": avg_quantity_per_ha,
            }
        )

    if not results:
        return None

    df = pd.DataFrame(results)
    df = df.sort_values(by="Custo estimado (R$)", ascending=False)
    return df
#

# Estado global para culturas da Fase 1
if "crops" not in st.session_state:
    st.session_state.crops = []


st.sidebar.title("📌 Navegação")
aba = st.sidebar.radio("Navegue pelas Fases:", [
    "🏠 Home",
    "🧮 Calculadora de Plantio (Fase 1)",
    "🚜 Gestão Completa (Fase 2)",
    "💧 Fase 3 — Sensores e Irrigação",
    "🤖 Fase 4 — Modelo Preditivo",
    "🪲 Fase 6 — Visão Computacional",
    "📨 Alertas AWS",
])


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
elif aba == "🧮 Calculadora de Plantio (Fase 1)":
    banner("Fase 1 — Calculadora de Plantio e Insumos (Simulação)", "#588157")

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
# FASE 2
# # =========================
elif aba == "🚜 Gestão Completa (Fase 2)":
    banner("Fase 2 — Gestão Agrícola Completa (Banco de Dados)", "#52796f")

    # -----------------------------
    # CULTURAS
    # -----------------------------
    st.subheader("🌱 Cadastro e gerenciamento de culturas")

    with st.form("fase2_form_cultura"):
        col1, col2 = st.columns(2)
        with col1:
            crop_name = st.text_input("Nome da cultura")
            planting_date = st.date_input("Data de plantio")
        with col2:
            harvest_date = st.date_input("Data de colheita (opcional)", value=None)
            area = st.number_input("Área (ha)", min_value=0.1, value=1.0, step=0.1)
            productivity = st.number_input("Produtividade estimada (t/ha)", min_value=0.1, value=5.0, step=0.1)

        submit_crop = st.form_submit_button("💾 Salvar cultura")

        if submit_crop:
            if not crop_name.strip():
                st.warning("Informe o nome da cultura.")
            else:
                crop_data = {
                    "name": crop_name.strip(),
                    "planting_date": planting_date.strftime("%Y-%m-%d"),
                    "harvest_date": harvest_date.strftime("%Y-%m-%d") if harvest_date else None,
                    "area": float(area),
                    "productivity": float(productivity),
                }
                save_crop_to_db(crop_data)
                st.success("Cultura salva com sucesso no banco de dados (Oracle).")

    # Listagem de culturas
    try:
        cultures = get_all_crops()
    except Exception as e:
        cultures = []
        st.error(f"Erro ao buscar culturas: {e}")

    st.markdown("### 📋 Culturas cadastradas")

    if cultures:
        df_crops = pd.DataFrame(cultures)
        # Ajuste de exibição de datas
        if "planting_date" in df_crops.columns:
            df_crops["planting_date"] = pd.to_datetime(df_crops["planting_date"]).dt.date
        if "harvest_date" in df_crops.columns:
            df_crops["harvest_date"] = pd.to_datetime(df_crops["harvest_date"]).dt.date

        df_crops = df_crops.rename(
            columns={
                "id": "ID",
                "name": "Cultura",
                "planting_date": "Plantio",
                "harvest_date": "Colheita",
                "area": "Área (ha)",
                "productivity": "Produtividade (t/ha)",
            }
        )
        st.dataframe(df_crops, use_container_width=True)
    else:
        st.info("Nenhuma cultura cadastrada ainda.")

    # Atualização de data de colheita
    st.markdown("#### ✏️ Atualizar data de colheita")

    if cultures:
        crop_options = {f"{c['id']} - {c['name']}": c["id"] for c in cultures}
        selected_crop_label = st.selectbox("Selecione a cultura", list(crop_options.keys()))
        selected_crop_id = crop_options[selected_crop_label]
        new_harvest_date = st.date_input("Nova data de colheita")

        if st.button("Atualizar colheita"):
            update_crop_harvest_date(selected_crop_id, new_harvest_date.strftime("%Y-%m-%d"))
            st.success("Data de colheita atualizada com sucesso.")
    else:
        st.info("Cadastre culturas para poder atualizar a data de colheita.")

    st.divider()

    # -----------------------------
    # INSUMOS
    # -----------------------------
    st.subheader("🧪 Cadastro e visualização de insumos")

    with st.form("fase2_form_insumo"):
        col1, col2, col3 = st.columns(3)
        with col1:
            input_name = st.text_input("Nome do insumo")
        with col2:
            input_type = st.text_input("Tipo (fertilizante, defensivo, etc.)")
        with col3:
            unit = st.text_input("Unidade (kg, L, etc.)", value="kg")

        unit_price = st.number_input("Preço unitário (R$)", min_value=0.0, value=10.0, step=0.1)

        submit_input = st.form_submit_button("💾 Salvar insumo")

        if submit_input:
            if not input_name.strip() or not input_type.strip() or not unit.strip():
                st.warning("Preencha nome, tipo e unidade do insumo.")
            else:
                data = {
                    "input_type": input_type.strip(),
                    "input_name": input_name.strip(),
                    "unit": unit.strip(),
                    "unit_price": float(unit_price),
                }
                save_input_to_db(data)
                st.success("Insumo salvo com sucesso no banco.")

    # Listagem de insumos
    try:
        inputs = get_all_inputs()
    except Exception as e:
        inputs = []
        st.error(f"Erro ao buscar insumos: {e}")

    st.markdown("### 📦 Insumos cadastrados")

    if inputs:
        df_inputs = pd.DataFrame(inputs).rename(
            columns={
                "id": "ID",
                "input_name": "Insumo",
                "input_type": "Tipo",
                "unit": "Unidade",
                "unit_price": "Preço unitário (R$)",
            }
        )
        st.dataframe(df_inputs, use_container_width=True)
    else:
        st.info("Nenhum insumo cadastrado ainda.")

    st.divider()

    # -----------------------------
    # APLICAÇÃO DE INSUMOS
    # -----------------------------
    st.subheader("🌿 Registrar aplicação de insumo em cultura")

    if not cultures or not inputs:
        st.info("Cadastre ao menos uma cultura e um insumo para registrar aplicações.")
    else:
        with st.form("fase2_form_aplicacao"):
            col1, col2 = st.columns(2)
            with col1:
                crop_options = {f"{c['id']} - {c['name']}": c["id"] for c in cultures}
                crop_label = st.selectbox("Cultura", list(crop_options.keys()))
                crop_id = crop_options[crop_label]
            with col2:
                input_options = {f"{i['id']} - {i['input_name']}": i["id"] for i in inputs}
                input_label = st.selectbox("Insumo", list(input_options.keys()))
                input_id = input_options[input_label]

            col3, col4, col5 = st.columns(3)
            with col3:
                quantity = st.number_input("Quantidade aplicada", min_value=0.1, value=1.0, step=0.1)
            with col4:
                application_date = st.date_input("Data da aplicação")
            with col5:
                recurrence = st.selectbox("Recorrência", ["Nenhuma", "Semanal", "Mensal"])

            recurrence_days = st.number_input(
                "Intervalo em dias (se recorrente)",
                min_value=0,
                value=0,
                step=1,
            )

            submit_app = st.form_submit_button("💾 Registrar aplicação")

            if submit_app:
                input_info = get_input_by_id(input_id)
                unit = input_info["unit"] if input_info else "unid"

                data = {
                    "crop_id": crop_id,
                    "input_id": input_id,
                    "quantity": float(quantity),
                    "unit": unit,
                    "application_date": application_date.strftime("%Y-%m-%d"),
                    "recurrence": recurrence if recurrence != "Nenhuma" else None,
                    "recurrence_days": int(recurrence_days) if recurrence != "Nenhuma" else None,
                }
                save_input_application_to_db(data)
                st.success("Aplicação registrada com sucesso no banco.")

    st.markdown("### 📜 Visão por cultura e insumo (relatórios)")

    if cultures:
        with st.expander("📋 Relatório por cultura"):
            for crop in cultures:
                st.markdown(f"**🌱 {crop['name']}**")
                try:
                    apps = get_applications_by_crop_id(crop["id"])
                except Exception as e:
                    st.error(f"Erro ao buscar aplicações para {crop['name']}: {e}")
                    continue

                if not apps:
                    st.info("Nenhuma aplicação registrada para esta cultura.")
                else:
                    df_apps = pd.DataFrame(apps).rename(
                        columns={
                            "input_name": "Insumo",
                            "input_type": "Tipo",
                            "quantity": "Quantidade",
                            "unit": "Unidade",
                            "application_date": "Data",
                        }
                    )
                    df_apps["Data"] = pd.to_datetime(df_apps["Data"]).dt.date
                    st.dataframe(df_apps, use_container_width=True)

    if inputs:
        with st.expander("📦 Relatório por insumo"):
            for ins in inputs:
                st.markdown(f"**🧪 {ins['input_name']} ({ins['input_type']})**")
                try:
                    apps = get_applications_by_input_id(ins["id"])
                except Exception as e:
                    st.error(f"Erro ao buscar aplicações para {ins['input_name']}: {e}")
                    continue

                if not apps:
                    st.info("Insumo ainda não aplicado em nenhuma cultura.")
                else:
                    df_apps = pd.DataFrame(apps).rename(
                        columns={
                            "crop_name": "Cultura",
                            "quantity": "Quantidade",
                            "unit": "Unidade",
                            "application_date": "Data",
                        }
                    )
                    df_apps["Data"] = pd.to_datetime(df_apps["Data"]).dt.date
                    st.dataframe(df_apps, use_container_width=True)

    st.divider()

    # -----------------------------
    # PREVISÃO (REGRESSÃO LINEAR)
    # -----------------------------
    st.subheader("📈 Previsão de demanda de insumos (Regressão Linear)")

    col_params, col_run = st.columns([2, 1])
    with col_params:
        target_area = st.number_input(
            "Área alvo para previsão (ha)",
            min_value=0.1,
            value=10.0,
            step=0.5,
        )
        target_productivity = st.number_input(
            "Produtividade alvo (t/ha)",
            min_value=0.1,
            value=6.0,
            step=0.1,
        )
    with col_run:
        run_forecast_btn = st.button("🚜 Rodar previsão")

    if run_forecast_btn:
        try:
            df_forecast = fase2_run_forecast(target_area, target_productivity)
        except Exception as e:
            df_forecast = None
            st.error(f"Erro ao executar previsão: {e}")

        if df_forecast is None:
            st.warning("Dados insuficientes para gerar previsões. Registre mais aplicações.")
        else:
            st.success("Previsão gerada com sucesso!")
            st.markdown("### 📊 Resultado por insumo")
            st.dataframe(df_forecast, use_container_width=True)

            st.markdown("### 💰 Custo estimado por insumo")
            st.bar_chart(
                df_forecast.set_index("Insumo")[["Custo estimado (R$)"]]
            )

            st.markdown("### ⭐ Índice de eficiência (IEI)")
            st.bar_chart(
                df_forecast.set_index("Insumo")[["Índice de eficiência (t/unidade)"]]
            )

            st.markdown("### 🌟 Destaques de eficiência")
            top_eff = df_forecast.sort_values(
                by="Índice de eficiência (t/unidade)", ascending=False
            ).head(3)

            for _, row in top_eff.iterrows():
                st.markdown(
                    f"""
                    - **{row['Insumo']}** ({row['Tipo']})
                      - Eficiência: **{row['Índice de eficiência (t/unidade)']:.2f}**
                      - Classificação: {row['Classificação de eficiência']}
                      - Uso médio: **{row['Uso médio por hectare (unidade/ha)']:.2f}**
                      - Custo estimado: **R$ {row['Custo estimado (R$)']:.2f}**
                    """
                )
#     else:
#         st.info("Defina o cenário de área e produtividade e clique em **Rodar previsão**.")

# =========================
# FASE 3 – MOCK (sensores + irrigação)
# =========================
elif aba == "💧 Fase 3 — Sensores e Irrigação":
    banner("Fase 3 — IoT com ESP32 (Sensores + Irrigação)", "#40916c")

    if not PHASE3_AVAILABLE:
        st.error(f"Erro ao carregar módulo da Fase 3: {PHASE3_ERROR}")
        st.info("Verifique se as dependências (oracledb, sqlalchemy, etc) estão instaladas e se o arquivo .env está configurado.")
    else:
        # --- MONITORAMENTO CLIMÁTICO ---
        c_header, c_btn = st.columns([3, 1])
        with c_header:
            st.subheader("🌤️ Monitoramento Climático")
        with c_btn:
            if st.button("🔄 Sincronizar Clima (API)"):
                with st.spinner("Buscando dados na OpenWeatherMap..."):
                    try:
                        # Importação tardia para evitar erro circular ou de dependência
                        from src.fase3.src.python.services.weather_service import run_weather_integration
                        run_weather_integration()
                        st.success("Dados climáticos atualizados!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro na sincronização: {e}")

        try:
            climate_records = climate_service.list_climate_data()
            climate_df = pd.DataFrame(climate_records)
        except Exception as e:
            st.error(f"Erro ao buscar dados climáticos: {e}")
            climate_df = pd.DataFrame()

        if not climate_df.empty:
            climate_df["timestamp"] = pd.to_datetime(climate_df["timestamp"])
            latest_climate = climate_df.sort_values("timestamp", ascending=False).iloc[0]
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Temperatura", f"{latest_climate['temperature']} °C")
            with c2:
                st.metric("Umidade do Ar", f"{latest_climate['air_humidity']}%")
            with c3:
                rain = "🌧️ Sim" if latest_climate['rain_forecast'] else "☀️ Não"
                st.metric("Previsão de Chuva", rain)
            with c4:
                st.caption(f"Atualizado em: {latest_climate['timestamp'].strftime('%d/%m/%Y %H:%M')}")
        else:
            st.info("Sem dados climáticos recentes.")

        st.markdown("---")
        
        # --- MONITORAMENTO DE SENSORES ---
        st.subheader("📡 Sensores IoT (Solo e Irrigação)")

        # Dados atuais dos sensores
        try:
            sensor_records = sensor_service.list_sensor_records()
            sensor_df = pd.DataFrame(sensor_records)
        except Exception as e:
            st.error(f"Erro ao buscar dados dos sensores: {e}")
            sensor_df = pd.DataFrame()

        if sensor_df.empty:
            st.info("Nenhum dado de sensor disponível. Utilize o simulador abaixo para gerar dados.")
        else:
            sensor_df["timestamp"] = pd.to_datetime(sensor_df["timestamp"])
            latest = sensor_df.sort_values("timestamp", ascending=False).iloc[0]
            
            st.subheader("🌱 Estado Atual da Safra (Última Leitura)")
            st.caption(f"Data/Hora: {latest['timestamp']}")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                # Gauge chart para umidade (usando métrica simples por enquanto para evitar dependência complexa de plotly no dashboard principal se não necessário)
                st.metric("Umidade do Solo", f"{latest['soil_moisture']:.1f}%", delta_color="normal")
                st.progress(min(int(latest['soil_moisture']), 100))
            
            with col2:
                st.metric("pH do Solo", f"{latest['soil_ph']:.2f}")
            
            with col3:
                phos = "✅ Presente" if latest["phosphorus_present"] else "❌ Ausente"
                st.metric("Fósforo (P)", phos)
            
            with col4:
                pot = "✅ Presente" if latest["potassium_present"] else "❌ Ausente"
                st.metric("Potássio (K)", pot)
            
            with col5:
                status = latest["irrigation_status"]
                emoji = "💧" if status == "ATIVADA" else "⛔"
                st.metric("Irrigação", f"{emoji} {status}")

            # --- MONITORAMENTO DE ALERTAS ---
            st.markdown("---")
            st.subheader("🚨 Monitoramento de Alertas")
            
            try:
                from src.final.aws_sns_service import get_sns_service
                sns_service = get_sns_service()
                
                alerts = []
                
                # Verificar condições críticas
                if latest['soil_ph'] < 5.5 or latest['soil_ph'] > 7.0:
                    alerts.append(("pH Crítico", latest))
                
                if latest['soil_moisture'] < 20:
                    alerts.append(("Seca Severa", latest))
                
                if latest['soil_moisture'] > 80:
                    alerts.append(("Encharcamento", latest))
                
                if not latest['phosphorus_present'] and not latest['potassium_present']:
                    alerts.append(("Deficiência Nutricional", latest))
                
                if latest['soil_moisture'] < 30 and latest['irrigation_status'] == "DESLIGADA":
                    alerts.append(("Falha na Irrigação", latest))
                
                # Exibir e enviar alertas automaticamente
                if alerts:
                    st.warning(f"⚠️ {len(alerts)} alerta(s) crítico(s) detectado(s)!")
                    
                    for alert_type, sensor_data in alerts:
                        col_alert, col_status = st.columns([3, 1])
                        with col_alert:
                            st.error(f"🚨 **{alert_type}**")
                        with col_status:
                            # Tentar enviar SNS automaticamente
                            if sns_service.send_sensor_alert(alert_type, dict(sensor_data)):
                                st.success("📧 SNS enviado")
                            else:
                                st.info("SNS não config.")
                else:
                    st.success("✅ Todos os parâmetros estão dentro do normal")
                    
            except Exception as e:
                st.error(f"Erro ao verificar alertas: {e}")


            # Gráficos Históricos
            st.subheader("📉 Histórico de Leituras")
            
            tab1, tab2 = st.tabs(["Umidade & pH", "Nutrientes & Irrigação"])
            
            with tab1:
                st.line_chart(sensor_df.set_index("timestamp")[["soil_moisture", "soil_ph"]])
            
            with tab2:
                st.write("Status de Irrigação ao longo do tempo")
                sensor_df['status_bin'] = sensor_df['irrigation_status'].apply(lambda x: 1 if x == "ATIVADA" else 0)
                st.area_chart(sensor_df.set_index("timestamp")[["status_bin"]])

        # --- SIMULADOR IOT ---
        st.markdown("---")
        st.subheader("🎮 Simulador IoT (Digital Twin)")
        with st.expander("Gerar nova leitura de sensor (Simulação de Hardware)"):
            with st.form("simulador_iot"):
                c1, c2 = st.columns(2)
                with c1:
                    sim_moisture = st.slider("Umidade do Solo (%)", 0.0, 100.0, 45.0)
                    sim_ph = st.slider("pH do Solo", 0.0, 14.0, 6.5)
                with c2:
                    sim_p = st.checkbox("Fósforo Presente", value=True)
                    sim_k = st.checkbox("Potássio Presente", value=True)
                    sim_irr = st.selectbox("Status Irrigação", ["DESLIGADA", "ATIVADA"])
                
                if st.form_submit_button("📡 Enviar Leitura"):
                    try:
                        # Pegar o primeiro sensor disponível ou criar um ID fictício
                        components = component_service.list_components()
                        sensor_id = None
                        for comp in components:
                            if comp.get('type') == 'Sensor':
                                sensor_id = comp['id']
                                break
                        
                        # Se não houver sensor cadastrado, usar um ID padrão
                        if not sensor_id:
                            sensor_id = "simulator-sensor-01"
                        
                        sensor_service.create_sensor_record({
                            "sensor_id": sensor_id,
                            "soil_moisture": sim_moisture,
                            "soil_ph": sim_ph,
                            "phosphorus_present": sim_p,
                            "potassium_present": sim_k,
                            "irrigation_status": sim_irr,
                            "timestamp": datetime.now()
                        })
                        st.success("Leitura enviada com sucesso para o banco de dados!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar leitura: {e}")


# =========================
# FASE 4 – MOCK (modelo preditivo)
# =========================
# =========================
# FASE 4 – MODELO PREDITIVO & IA
# =========================
elif aba == "🤖 Fase 4 — Modelo Preditivo":
    banner("Fase 4 — Inteligência Artificial e Análises", "#7209b7")
    
    st.markdown("""
    Esta fase utiliza **Machine Learning (Random Forest)** para analisar o histórico de dados 
    e prever a necessidade de irrigação com base em múltiplas variáveis.
    """)

    if not PHASE3_AVAILABLE:
        st.error("O módulo de ML depende dos serviços da Fase 3, que não foram carregados corretamente.")
    else:
        # Status do modelo
        try:
            model_status = ml_service.get_model_status()
        except Exception as e:
            st.error(f"Erro ao verificar status do modelo: {e}")
            model_status = {"model_loaded": False}

        # --- ABAS INTERNAS DA FASE 4 ---
        tab_ml, tab_analytics = st.tabs(["🧠 Treinamento & Simulador", "📊 Análises Avançadas"])

        with tab_ml:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Status do Modelo")
                if model_status["model_loaded"]:
                    st.success("✅ Modelo carregado e pronto para uso")
                    st.info(f"📁 Caminho: {model_status.get('model_path', 'N/A')}")
                else:
                    st.warning("⚠️ Modelo não treinado")
                    st.info("Treine o modelo com dados históricos para ativar predições")
            
            with col2:
                st.subheader("🎯 Treinar Modelo")
                if st.button("🚀 Treinar Modelo com Dados Históricos"):
                    with st.spinner("Treinando modelo..."):
                        try:
                            sensor_data = sensor_service.list_sensor_records()
                            climate_data = climate_service.list_climate_data()
                            
                            result = ml_service.train_model(sensor_data, climate_data)
                            
                            if result["success"]:
                                st.success("✅ Modelo treinado com sucesso!")
                                c1, c2, c3 = st.columns(3)
                                c1.metric("Acurácia", f"{result['accuracy']:.1%}")
                                c2.metric("Amostras Treino", result['training_samples'])
                                c3.metric("Amostras Teste", result['test_samples'])
                                
                                with st.expander("📋 Relatório de Classificação"):
                                    st.text(result['classification_report'])
                            else:
                                st.error(f"❌ Erro no treinamento: {result['message']}")
                        except Exception as e:
                            st.error(f"Erro crítico ao treinar: {e}")

            st.markdown("---")

            # Feature Importance
            if model_status["model_loaded"]:
                st.subheader("📈 O que influencia a decisão?")
                try:
                    importance = ml_service.get_feature_importance()
                    if importance:
                        fig = px.bar(
                            x=list(importance.values()),
                            y=list(importance.keys()),
                            orientation='h',
                            title="Importância das Variáveis no Modelo",
                            labels={'x': 'Importância', 'y': 'Variável'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Não foi possível gerar gráfico de importância: {e}")
            
            # Simulador de Predição
            st.subheader("🎮 Simulador de Predição (What-If)")
            st.markdown("Teste diferentes cenários para ver a decisão da IA:")
            
            with st.form("simulador_ml"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    s_moist = st.slider("Umidade Solo (%)", 0, 100, 45)
                    s_ph = st.slider("pH Solo", 0.0, 14.0, 6.5)
                    s_p = st.checkbox("Fósforo?", value=True)
                with c2:
                    s_k = st.checkbox("Potássio?", value=True)
                    s_temp = st.slider("Temperatura (°C)", -10, 50, 25)
                    s_hum = st.slider("Umidade Ar (%)", 0, 100, 60)
                with c3:
                    s_rain = st.checkbox("Chuva Prevista?", value=False)
                    s_hour = st.slider("Hora", 0, 23, 12)
                    s_month = st.slider("Mês", 1, 12, 6)
                
                if st.form_submit_button("🔮 Prever Ação"):
                    if model_status["model_loaded"]:
                        try:
                            pred = ml_service.predict_irrigation(
                                s_moist, s_ph, s_p, s_k, s_temp, s_hum, s_rain, s_hour, s_month
                            )
                            if pred["success"]:
                                decision = "💧 IRRIGAR" if pred["should_irrigate"] else "⛔ NÃO IRRIGAR"
                                color = "green" if pred["should_irrigate"] else "red"
                                st.markdown(f"<h2 style='color: {color}; text-align: center;'>{decision}</h2>", unsafe_allow_html=True)
                                st.metric("Confiança da IA", f"{pred['confidence']:.1%}")
                        except Exception as e:
                            st.error(f"Erro na predição: {e}")
                    else:
                        st.error("Treine o modelo primeiro!")

        with tab_analytics:
            st.subheader("🔍 Análise de Correlações")
            try:
                sensor_recs = sensor_service.list_sensor_records()
                climate_recs = climate_service.list_climate_data()
                
                if sensor_recs and climate_recs:
                    df_s = pd.DataFrame(sensor_recs)
                    df_c = pd.DataFrame(climate_recs)
                    
                    df_s["timestamp"] = pd.to_datetime(df_s["timestamp"])
                    df_c["timestamp"] = pd.to_datetime(df_c["timestamp"])
                    
                    # Aproximação por hora para merge
                    df_s['ts_h'] = df_s['timestamp'].dt.floor('h')
                    df_c['ts_h'] = df_c['timestamp'].dt.floor('h')
                    
                    merged = pd.merge(df_s, df_c, left_on='ts_h', right_on='ts_h', how='inner')
                    
                    if not merged.empty:
                        corr_cols = ['soil_moisture', 'soil_ph', 'temperature', 'air_humidity']
                        corr_matrix = merged[corr_cols].corr()
                        
                        fig_corr = px.imshow(corr_matrix, text_auto=True, title="Matriz de Correlação", color_continuous_scale='RdBu_r')
                        st.plotly_chart(fig_corr, use_container_width=True)
                        
                        st.subheader("💧 Padrões de Irrigação")
                        fig_scatter = px.scatter(merged, x="soil_moisture", y="temperature", color="irrigation_status",
                                               title="Dispersão: Umidade x Temperatura (por Status Irrigação)")
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    else:
                        st.info("Não há dados coincidentes (mesma hora) entre sensores e clima para correlação.")
                else:
                    st.info("Dados insuficientes para análise avançada.")
            except Exception as e:
                st.error(f"Erro ao gerar análises: {e}")

# =========================
# FASE 6 – VISÃO COMPUTACIONAL
# =========================
elif aba == "🪲 Fase 6 — Visão Computacional":
    banner("Fase 6 — Detecção de Pragas e Animais (YOLO)", "#e63946")
    
    st.info("Esta fase utiliza Visão Computacional para analisar imagens enviadas e detectar animais ou pragas.")

    uploaded_file = st.file_uploader("Envie uma imagem para análise", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Imagem Original")
            st.image(uploaded_file, use_container_width=True)
        
        with col2:
            st.subheader("Resultado da Análise")
            if st.button("🔍 Analisar Imagem"):
                with st.spinner("Processando imagem com YOLO..."):
                    try:
                        # Importação tardia para evitar erro se cv2/ultralytics não estiver instalado no início
                        from src.fase6.src.computer_vision_service import ComputerVisionService
                        from src.final.aws_sns_service import get_sns_service
                        
                        # Instanciar serviço (pode demorar um pouco na primeira vez para baixar o modelo)
                        cv_service = ComputerVisionService()
                        sns_service = get_sns_service()
                        
                        # Ler bytes do arquivo
                        bytes_data = uploaded_file.getvalue()
                        
                        # Analisar
                        annotated_img, detections = cv_service.analyze_image(bytes_data)
                        
                        if annotated_img:
                            st.image(annotated_img, caption="Imagem Anotada", use_container_width=True)
                            
                            if detections:
                                st.success(f"Detectados: {len(detections)} objetos.")
                                
                                # Verificar se há animais (pragas potenciais)
                                animal_classes = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'mouse', 'rat']
                                detected_animals = [d for d in detections if d['class'] in animal_classes]
                                
                                # Mostrar todas as detecções
                                for det in detections:
                                    emoji = "🚨" if det['class'] in animal_classes else "✅"
                                    st.write(f"{emoji} **{det['class']}** ({det['confidence']:.2f})")
                                
                                # Disparar alerta se houver animais
                                if detected_animals:
                                    st.warning(f"⚠️ {len(detected_animals)} animal(is) detectado(s)! Disparan do alerta SNS...")
                                    alert_sent = sns_service.send_pest_alert(detected_animals)
                                    if alert_sent:
                                        st.success("📧 Alerta SNS enviado com sucesso!")
                                    else:
                                        st.info("SNS não configurado. Alerta não enviado.")
                            else:
                                st.info("Nenhum objeto detectado na imagem.")
                        else:
                            st.warning("Não foi possível processar a imagem.")
                            
                    except ImportError:
                        st.error("Bibliotecas da Fase 6 (opencv, ultralytics) não encontradas.")
                        st.code("pip install opencv-python ultralytics")
                    except Exception as e:
                        st.error(f"Erro durante a análise: {e}")


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
