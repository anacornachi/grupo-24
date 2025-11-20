from sklearn.linear_model import LinearRegression
import numpy as np
from src.fase2.src.repositories.prediction import get_historical_input_data


def predict_demand():
    print("\n📈 Previsão de demanda e análises preditivas\n")
    print("📌 Cenário base para previsão: 10 hectares, 6 toneladas por hectare\n")

    try:
        rows = get_historical_input_data()
    except Exception as e:
        print(f"❌ Erro ao buscar dados para previsão: {e}")
        return

    if not rows:
        print("⚠️ Dados insuficientes para realizar previsão.")
        return

    insumo_data = {}
    for row in rows:
        area, produtividade, input_name, input_type, unit, unit_price, quantity = row
        if input_name not in insumo_data:
            insumo_data[input_name] = {
                "X": [],
                "y": [],
                "unit": unit,
                "unit_price": unit_price,
                "input_type": input_type
            }
        insumo_data[input_name]["X"].append([area, produtividade])
        insumo_data[input_name]["y"].append(quantity)

    print("📊 Previsões personalizadas por insumo:")
    for input_name, data in insumo_data.items():
        x = np.array(data["X"])
        y = np.array(data["y"])
        model = LinearRegression()
        model.fit(x, y)

        predicted_quantity = model.predict([[10, 6]])[0]
        estimated_cost = predicted_quantity * data["unit_price"]

        print(f"\n🧪 Insumo: {input_name} ({data['input_type']})")
        print(f"  ✅ Quantidade prevista: {predicted_quantity:.2f} {data['unit']}")
        print(f"  💰 Custo estimado: R$ {estimated_cost:.2f} (R$ {data['unit_price']:.2f} por {data['unit']})")

        total_productivity = sum([x[1] for x in data["X"]])
        total_quantity = sum(data["y"])
        iei = total_productivity / total_quantity if total_quantity else 0

        if iei > 0.5:
            classificacao = "🌟 Alta eficiência"
        elif iei >= 0.3:
            classificacao = "⚖️ Média eficiência"
        else:
            classificacao = "❗Baixa eficiência"

        print(f"  📊 Índice de eficiência (histórico): {iei:.2f} t por {data['unit']}")
        print(f"  🧠 Classificação: {classificacao}")

    print("\n📈 Análises complementares:")

    for input_name, data in insumo_data.items():
        total_quantity = sum(data["y"])
        total_area = sum([x[0] for x in data["X"]])
        avg_quantity_per_ha = total_quantity / total_area if total_area else 0

        print(f"\n📌 {input_name}")
        print(f"  📉 Uso médio por hectare: {avg_quantity_per_ha:.2f} {data['unit']}/ha")

    print(
        "\nℹ️ Interpretação:\n  - Índice de eficiência: quanto sua cultura produziu por unidade de insumo aplicada\n  - Uso médio/ha: referência para escalonar e planejar novas safras")
    print("\n✅ Fim da análise preditiva.")