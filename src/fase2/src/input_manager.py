
from src.schemas.custom_validator import CustomValidator
from src.fase2.src.validations import prompt_and_validate, validate_with_schema
from src.fase2.src.schemas.input_schema import input_schema, application_schema
from src.fase2.src.repositories.input import (
    save_input_to_db,
    get_all_inputs,
    save_input_application_to_db,
    get_input_by_id
)
from src.fase2.src.repositories.crop import get_all_cropsidate_with_schema
from src.files import load_json_list
import os

def register_input():
    print("\n🧪 Cadastro de Insumo (catálogo)")
    fields = ["input_type", "input_name", "unit", "unit_price"]

    validated_data = prompt_and_validate(input_schema, fields)

    if validated_data:
        save_input_to_db(validated_data)
        print("✅ Insumo cadastrado com sucesso no catálogo!\n")

        should_link = input("Deseja vincular este insumo a alguma cultura agora? (s/n): ").strip().lower()
        if should_link == "s":
            apply_input_to_crop()
        else:
            print("👍 Cadastro finalizado. Você pode vincular este insumo mais tarde.\n")


def apply_input_to_crop():
    print("\n🔗 Vincular insumo a cultura")

    try:
        crops = get_all_crops()
        inputs = get_all_inputs()
    except Exception as e:
        print("❌ Não foi possível acessar o banco de dados agora. Tente novamente mais tarde.")

    if not crops or not inputs:
        print("⚠️ É necessário ter pelo menos uma cultura e um insumo cadastrados.")
        return

    print("\n🌱 Culturas disponíveis:")
    for c in crops:
        print(f"{c['id']}: {c['name']}")

    print("\n🧪 Insumos disponíveis:")
    for i in inputs:
        print(f"{i['id']}: {i['input_name']} ({i['input_type']})")

    fields = [
        "crop_id",
        "input_id",
        "quantity",
        "application_date",
        "recurrence",
        "recurrence_days"
    ]

    result = {}

    for field in fields:
        original_schema = application_schema[field]
        field_schema = application_schema[field].copy()
        field_schema["required"] = False

        label = {
            "crop_id": "Número da cultura: ",
            "input_id": "Número do insumo: ",
            "application_date": "Data da aplicação (AAAA-MM-DD): ",
            "recurrence": "Frequência da aplicação (única, semanal, quinzenal, mensal): ",
            "recurrence_days": "Intervalo (em dias) entre aplicações: ",
        }.get(field, "")

        if field == "quantity":
            unit = get_input_by_id(result["input_id"])["unit"]
            label = f"Quantidade aplicada (em {unit}): "

        while True:
            value = input(label).strip()

            if field == "application_date" and value:
                from datetime import datetime
                try:
                    datetime.strptime(value, "%Y-%m-%d")
                except ValueError:
                    print("❌ Formato inválido. Use o formato AAAA-MM-DD.")
                    continue

            if field in ["unit", "input_type", "recurrence"]:
                value = value.lower()

            if field_schema["type"] == "float":
                try:
                    value = float(value)
                except ValueError:
                    print("❌ Valor inválido. Digite um número com ponto decimal.")
                    continue

            if field_schema["type"] == "integer":
                try:
                    value = int(value)
                except ValueError:
                    print("❌ Valor inválido. Digite um número inteiro.")
                    continue

            if value == "":
                value = None

            validator = CustomValidator({field: field_schema})
            if validator.validate({field: value}):
                if value is None and original_schema.get("nullable") is not True:
                    print("❌ Campo obrigatório.")
                    continue
                result[field] = value
                break
            else:
                print("❌ Valor inválido.")
                continue

    result["unit"] = get_input_by_id(result["input_id"])["unit"]

    save_input_application_to_db(result)
    print("✅ Insumo aplicado à cultura com sucesso!\n")


def import_inputs_from_json():
    print("\n📥 Importação de insumos via JSON")
    path = input("Informe o caminho do arquivo: ").strip()

    if not os.path.exists(path):
        print("❌ Arquivo não encontrado.")
        return

    data = load_json_list(path)
    if not data:
        print("⚠️ Nenhum dado válido encontrado.")
        return

    success, failure = 0, 0

    for i, item in enumerate(data, start=1):
        is_valid, result = validate_with_schema(input_schema, item)
        if is_valid:
            save_input_to_db(result)
            success += 1
        else:
            print(f"\n❌ Erros no registro {i}:")
            print(f"📌 Dados recebidos: {item}")
            for field, errors in result.items():
                print(f" - Campo '{field}':")
                for msg in errors:
                    print(f"   • {msg}")
            failure += 1

    print(f"\n✅ {success} insumo(s) importado(s) com sucesso.")
    print(f"❌ {failure} com erro(s) e não foram importados.")
