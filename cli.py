# cli.py
"""Interface de Linha de Comandos (CLI) do Gerenciador de Frota.

Uso:
    python cli.py                      # menu interativo
    python cli.py seed                 # carrega dados de exemplo
    python cli.py relatorio consumo    # status|custos|eficiencia|viagens|km|consumo|todos
    python cli.py cadastrar-veiculo carro ABC1D23 Toyota Corolla 2022 10000 12.5
    python cli.py abastecer ABC1D23 40 240.50 --combustivel gasolina
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from typing import Callable

from src.excecoes import FrotaError
from src.repositorios.base import RepositorioBase
from src.repositorios.json_repository import JsonRepository
from src.repositorios.sqlite_repository import SqliteRepository
from src.servicos.frota_service import FrotaService
from src.servicos.relatorios import NOMES_RELATORIOS


# --- Utilitários de entrada ---
def ler_texto(msg: str) -> str:
    return input(f"{msg}: ").strip()


def _ler_numero(msg: str, conversor: Callable[[str], float]) -> float:
    while True:
        try:
            return conversor(input(f"{msg}: ").strip().replace(",", "."))
        except ValueError:
            print("Valor numérico inválido, tente novamente.")


def ler_float(msg: str) -> float:
    return _ler_numero(msg, float)


def ler_int(msg: str) -> int:
    return int(_ler_numero(msg, int))


def hoje() -> str:
    return date.today().strftime("%d/%m/%Y")


# --- Ações do menu ---
def cadastrar_veiculo(svc: FrotaService) -> None:
    print("\n[ CADASTRO DE VEÍCULO ]")
    tipo = ler_texto("Tipo (carro/moto/caminhao)")
    v = svc.cadastrar_veiculo(
        tipo, ler_texto("Placa"), ler_texto("Marca"), ler_texto("Modelo"),
        ler_int("Ano"), ler_float("Quilometragem atual"), ler_float("Consumo médio (km/l)"),
    )
    print(f"Cadastrado: {v}")


def listar_veiculos(svc: FrotaService) -> None:
    print("\n[ VEÍCULOS ]")
    for v in sorted(svc.veiculos):
        extra = f" | Motorista: {v.motorista_alocado.nome}" if v.motorista_alocado else ""
        print(f"{v}{extra}")
    if not svc.veiculos:
        print("Nenhum veículo registrado.")


def atualizar_veiculo(svc: FrotaService) -> None:
    placa = ler_texto("Placa do veículo")
    campo = ler_texto("Campo (marca/modelo/ano/quilometragem/consumo_medio)")
    if campo in ("ano",):
        valor = ler_int("Novo valor")
    elif campo in ("quilometragem", "consumo_medio"):
        valor = ler_float("Novo valor")
    else:
        valor = ler_texto("Novo valor")
    print(f"Atualizado: {svc.atualizar_veiculo(placa, **{campo: valor})}")


def remover_veiculo(svc: FrotaService) -> None:
    svc.remover_veiculo(ler_texto("Placa do veículo"))
    print("Veículo removido.")


def cadastrar_motorista(svc: FrotaService) -> None:
    print("\n[ CADASTRO DE MOTORISTA ]")
    m = svc.cadastrar_motorista(
        ler_texto("Nome"), ler_texto("CPF"), ler_texto("Categoria da CNH (A-E)"),
        ler_int("Tempo de experiência (anos)"),
    )
    print(f"Cadastrado: {m}")


def listar_motoristas(svc: FrotaService) -> None:
    print("\n[ MOTORISTAS ]")
    for m in svc.motoristas:
        print(f"{m} | CPF: {m.cpf}")
    if not svc.motoristas:
        print("Nenhum motorista registrado.")


def editar_motorista(svc: FrotaService) -> None:
    cpf = ler_texto("CPF do motorista")
    campo = ler_texto("Campo (nome/cnh_categoria/tempo_experiencia_anos)")
    valor = ler_int("Novo valor") if campo == "tempo_experiencia_anos" else ler_texto("Novo valor")
    print(f"Atualizado: {svc.editar_motorista(cpf, **{campo: valor})}")


def remover_motorista(svc: FrotaService) -> None:
    svc.remover_motorista(ler_texto("CPF do motorista"))
    print("Motorista removido.")


def alocar(svc: FrotaService) -> None:
    v = svc.alocar(ler_texto("Placa do veículo"), ler_texto("CPF do motorista"))
    print(f"Veículo {v.placa} alocado a {v.motorista_alocado.nome}.")


def registrar_viagem(svc: FrotaService) -> None:
    viagem = svc.registrar_viagem(
        ler_texto("Placa do veículo"), ler_texto("Origem"),
        ler_texto("Destino"), ler_float("Distância percorrida (km)"),
    )
    print(f"{viagem} registrada. Quilometragem atualizada.")


def liberar(svc: FrotaService) -> None:
    svc.liberar(ler_texto("Placa do veículo"))
    print("Veículo liberado e motorista disponível.")


def abastecer(svc: FrotaService) -> None:
    svc.registrar_abastecimento(
        ler_texto("Placa do veículo"), ler_float("Litros"), ler_float("Valor pago (R$)"),
        ler_texto("Combustível") or "gasolina",
    )
    print("Abastecimento registrado.")


def enviar_manutencao(svc: FrotaService) -> None:
    placa = ler_texto("Placa do veículo")
    tipo = ler_texto("Tipo (preventiva/corretiva)")
    descricao = ler_texto("Descrição")
    estrategia = ler_texto("Complexidade (basica/complexa/pesada)") or "basica"
    pecas = ler_float("Custo de peças (R$)")
    m = svc.enviar_para_manutencao(placa, tipo, descricao, estrategia, pecas)
    print(f"Veículo em manutenção. {m}")


def concluir_manutencao(svc: FrotaService) -> None:
    svc.concluir_manutencao(ler_texto("Placa do veículo"))
    print("Manutenção concluída. Veículo ATIVO.")


def desativar(svc: FrotaService) -> None:
    svc.desativar_veiculo(ler_texto("Placa do veículo"))
    print("Veículo desativado.")


def historico(svc: FrotaService) -> None:
    v = svc.buscar_veiculo(ler_texto("Placa do veículo"))
    print(f"\n[ HISTÓRICO DE {v.placa} ]")
    for e in v.historico_eventos:
        print(e)


def relatorios(svc: FrotaService) -> None:
    nome = ler_texto(f"Relatório ({'/'.join(NOMES_RELATORIOS)}/todos)")
    print()
    print(svc.gerar_relatorio(nome))


def seed(svc: FrotaService) -> None:
    print("Dados de exemplo carregados." if svc.popular_seed()
          else "Já existem dados; seed ignorado.")


OPCOES: dict[str, tuple[str, Callable[[FrotaService], None]]] = {
    "1": ("Cadastrar veículo", cadastrar_veiculo),
    "2": ("Listar veículos", listar_veiculos),
    "3": ("Atualizar veículo", atualizar_veiculo),
    "4": ("Remover veículo", remover_veiculo),
    "5": ("Cadastrar motorista", cadastrar_motorista),
    "6": ("Listar motoristas", listar_motoristas),
    "7": ("Editar motorista", editar_motorista),
    "8": ("Remover motorista", remover_motorista),
    "9": ("Alocar motorista a veículo", alocar),
    "10": ("Registrar viagem", registrar_viagem),
    "11": ("Liberar veículo (devolução)", liberar),
    "12": ("Registrar abastecimento", abastecer),
    "13": ("Enviar veículo para manutenção", enviar_manutencao),
    "14": ("Concluir manutenção", concluir_manutencao),
    "15": ("Desativar veículo", desativar),
    "16": ("Histórico de eventos do veículo", historico),
    "17": ("Relatórios", relatorios),
    "18": ("Carregar dados de exemplo (seed)", seed),
}


def exibir_menu() -> str:
    print("\n--- SISTEMA DE GERENCIAMENTO DE FROTA ---")
    for chave, (rotulo, _) in OPCOES.items():
        print(f"{chave:>2}. {rotulo}")
    print(" 0. Sair")
    return input("Escolha uma opção: ").strip()


def menu_interativo(svc: FrotaService) -> None:
    while True:
        try:
            opcao = exibir_menu()
            if opcao == "0":
                print("A encerrar o sistema...")
                return
            if opcao not in OPCOES:
                print("Opção inválida, tente novamente.")
                continue
            OPCOES[opcao][1](svc)
        except (FrotaError, ValueError, TypeError) as erro:
            print(f"Erro: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nA encerrar o sistema...")
            return


# --- Subcomandos (frota <comando>) ---
def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="frota", description="Gerenciador de Frota")
    p.add_argument("--backend", choices=["json", "sqlite"], default="json")
    p.add_argument("--arquivo", default=None, help="Caminho do arquivo de dados")
    sub = p.add_subparsers(dest="comando")
    sub.add_parser("menu", help="Menu interativo (padrão)")
    sub.add_parser("seed", help="Carrega dados de exemplo")

    cv = sub.add_parser("cadastrar-veiculo", help="Cadastra um veículo")
    cv.add_argument("tipo", choices=["carro", "moto", "caminhao"])
    cv.add_argument("placa")
    cv.add_argument("marca")
    cv.add_argument("modelo")
    cv.add_argument("ano", type=int)
    cv.add_argument("km", type=float)
    cv.add_argument("consumo", type=float)

    ab = sub.add_parser("abastecer", help="Registra um abastecimento")
    ab.add_argument("placa")
    ab.add_argument("litros", type=float)
    ab.add_argument("valor", type=float)
    ab.add_argument("--combustivel", default="gasolina")

    rel = sub.add_parser("relatorio", help="Gera um relatório")
    rel.add_argument("nome", choices=[*NOMES_RELATORIOS, "todos"])
    return p


def criar_repositorio(backend: str, arquivo: str | None) -> RepositorioBase:
    if backend == "sqlite":
        return SqliteRepository(arquivo or "dados_frota.db")
    return JsonRepository(arquivo or "dados_frota.json")


def main(argv: list[str] | None = None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        svc = FrotaService(criar_repositorio(args.backend, args.arquivo))
        if args.comando in (None, "menu"):
            menu_interativo(svc)
        elif args.comando == "seed":
            seed(svc)
        elif args.comando == "cadastrar-veiculo":
            print(f"Cadastrado: {svc.cadastrar_veiculo(args.tipo, args.placa, args.marca, args.modelo, args.ano, args.km, args.consumo)}")
        elif args.comando == "abastecer":
            svc.registrar_abastecimento(args.placa, args.litros, args.valor, args.combustivel)
            print("Abastecimento registrado.")
        elif args.comando == "relatorio":
            print(svc.gerar_relatorio(args.nome))
    except (FrotaError, ValueError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())