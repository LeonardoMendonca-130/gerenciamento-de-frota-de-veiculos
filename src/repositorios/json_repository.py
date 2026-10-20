"""Módulo para persistência de dados em JSON."""
import json
import os
from src.modelos.veiculo import Carro, Moto, Caminhao

class JsonRepository:
    """Responsável por ler e gravar dados num ficheiro JSON."""

    def __init__(self, caminho_ficheiro: str = "dados_frota.json"):
        self.caminho_ficheiro = caminho_ficheiro
        # Cria o ficheiro vazio caso não exista
        if not os.path.exists(self.caminho_ficheiro):
            self.salvar_dados({"veiculos": []})

    def salvar_dados(self, dados: dict) -> None:
        """Escreve um dicionário no ficheiro usando json.dump."""
        with open(self.caminho_ficheiro, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def ler_dados(self) -> dict:
        """Lê o ficheiro JSON e devolve um dicionário usando json.load."""
        with open(self.caminho_ficheiro, 'r', encoding='utf-8') as f:
            return json.load(f)

    def guardar_veiculos(self, lista_veiculos: list) -> None:
        """Converte uma lista de objetos Veiculo em dicionários e guarda-os."""
        dados_formatados = []
        for v in lista_veiculos:
            tipo_veiculo = v.__class__.__name__
            dados_formatados.append({
                "tipo": tipo_veiculo,
                "placa": v.placa,
                "marca": v.marca,
                "modelo": v.modelo,
                "ano": v.ano,
                "quilometragem": v.quilometragem,
                "consumo_medio": v.consumo_medio,
                "status": v.status
            })
        
        dados_atuais = self.ler_dados()
        dados_atuais["veiculos"] = dados_formatados
        self.salvar_dados(dados_atuais)