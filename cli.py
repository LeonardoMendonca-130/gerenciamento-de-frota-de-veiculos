"""Interface de Linha de Comandos (CLI) para o Gerenciador de Frota."""

import sys
from src.repositorios.json_repository import JsonRepository
from src.modelos.veiculo import Carro

def exibir_menu():
    print("\n--- SISTEMA DE GERENCIAMENTO DE FROTA ---")
    print("1. Cadastrar Veículo (Carro)")
    print("2. Relatório da Frota")
    print("3. Sair")
    return input("Escolha uma opção: ")

def cadastrar_veiculo(repo):
    print("\n[ CADASTRO DE VEÍCULO ]")
    placa = input("Placa: ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    ano = int(input("Ano: "))
    km = float(input("Quilometragem atual: "))
    consumo = float(input("Consumo médio (km/l): "))
    
    # Cria o objeto e guarda no ficheiro JSON
    novo_carro = Carro(placa, marca, modelo, ano, km, consumo)
    dados = repo.ler_dados()
    veiculos = dados.get("veiculos", [])
    
    veiculos.append({
        "tipo": "Carro", "placa": novo_carro.placa, "marca": novo_carro.marca,
        "modelo": novo_carro.modelo, "ano": novo_carro.ano,
        "quilometragem": novo_carro.quilometragem, "status": novo_carro.status
    })
    
    dados["veiculos"] = veiculos
    repo.salvar_dados(dados)
    print("Veículo cadastrado com sucesso!")

def relatorio_frota(repo):
    print("\n[ RELATÓRIO DE FROTA ]")
    dados = repo.ler_dados()
    for v in dados.get("veiculos", []):
        print(f"Placa: {v['placa']} | Modelo: {v['modelo']} | Status: {v['status']}")

def main():
    repo = JsonRepository()
    
    while True:
        opcao = exibir_menu()
        if opcao == "1":
            cadastrar_veiculo(repo)
        elif opcao == "2":
            relatorio_frota(repo)
        elif opcao == "3":
            print("A encerrar o sistema...")
            sys.exit(0)
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()