""" Relatório inicial da frota."""
from src.repositorios.json_repository import JsonRepository

def exibir_relatorio_status():
    """Lê os veículos do ficheiro JSON e agrupa-os por estado."""
    repo = JsonRepository()
    dados = repo.ler_dados()
    veiculos = dados.get("veiculos", [])

    if not veiculos:
        print("Nenhum veículo registado.")
        return

    ativos = [v for v in veiculos if v["status"] == "ATIVO"]
    manutencao = [v for v in veiculos if v["status"] == "MANUTENCAO"]
    inativos = [v for v in veiculos if v["status"] == "INATIVO"]

    print("=" * 40)
    print("RELATÓRIO INICIAL DE VEÍCULOS")
    print("=" * 40)
    print(f"\n[ VEÍCULOS ATIVOS ]: {len(ativos)}")
    for v in ativos:
        print(f"  - {v['placa']} ({v['modelo']})")

    print(f"\n[ EM MANUTENÇÃO ]: {len(manutencao)}")
    for v in manutencao:
        print(f"  - {v['placa']} ({v['modelo']})")

    print(f"\n[ VEÍCULOS INATIVOS ]: {len(inativos)}")
    for v in inativos:
        print(f"  - {v['placa']} ({v['modelo']})")

if __name__ == "__main__":
    exibir_relatorio_status()