from datetime import datetime

from src.fase2.src.validations import prompt_and_validate, validate_with_schema
from src.schemas.crop_schema import crop_schema
from src.files import load_json_list

from src.fase2.src.repositories.crop import save_crop_to_db, get_all_crops, update_crop_harvest_date


def register_crop():
    print("\n🌱 Cadastro de Cultura Agrícola")
    fields = ["name", "planting_date", "harvest_date", "area", "productivity"]

    validated_data = prompt_and_validate(crop_schema, fields)
    if validated_data:
        save_crop_to_db(validated_data)
        print("✅ Cultura cadastrada com sucesso!\n")


def import_crops_from_json():
    print("\n Importação de culturas via JSON")
    path = input("Informe o caminho do arquivo: ").strip()
    data = load_json_list(path)

    if not data:
        print("⚠️ Nenhum dado válido encontrado.")
        return

    success, failure = 0, 0
    for i, item in enumerate(data, start=1):
        is_valid, result = validate_with_schema(crop_schema, item)
        if is_valid:
            save_crop_to_db(result)
            success += 1
        else:
            print(f"\n❌ Erros no registro {i}:")
            print(f"📌 Dados recebidos: {item}")
            for field, msgs in result.items():
                print(
                    f" - Campo '{field}' com valor '{item.get(field, 'N/A')}' apresentou:"
                )
                for msg in msgs:
                    print(f"   • {msg}")
            failure += 1

    if success:
        print(f"\n✅ {success} cultura(s) importada(s) com sucesso.")
    if failure:
        print(f"❌ {failure} cultura(s) com erro(s) e não foram importadas.")


def update_harvest_date():
    print("\n🌾 Atualizar data de colheita de uma cultura")

    try:
        cultures = get_all_crops()
    except Exception as e:
        print(f"❌ Erro ao buscar culturas: {e}")
        return

    if not cultures:
        print("⚠️ Nenhuma cultura cadastrada.")
        return

    print("\n🌱 Culturas disponíveis:")
    for crop in cultures:
        status = "✅" if crop.get("harvest_date") else "⏳"
        print(f"{crop['id']}: {crop['name']} (Plantio: {crop['planting_date'].strftime('%Y-%m-%d')}) {status}")

    try:
        crop_id = int(input("\nDigite o número da cultura que deseja atualizar: ").strip())
    except ValueError:
        print("❌ Entrada inválida. Use um número.")
        return

    matching_crop = next((c for c in cultures if c["id"] == crop_id), None)
    if not matching_crop:
        print("❌ Cultura não encontrada.")
        return

    if matching_crop["harvest_date"]:
        print("⚠️ Esta cultura já possui data de colheita.")
        overwrite = input("Deseja sobrescrever a data atual? (s/n): ").strip().lower()
        if overwrite != "s":
            print("❌ Atualização cancelada.")
            return

    while True:
        new_date_str = input("Informe a nova data de colheita (AAAA-MM-DD): ").strip()
        try:
            datetime.strptime(new_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("❌ Formato inválido. Use o formato AAAA-MM-DD.")

    try:
        update_crop_harvest_date(crop_id, new_date_str)
        print("✅ Data de colheita atualizada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao atualizar a cultura: {e}")
