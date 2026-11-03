# src/modelos/__init__.py
"""Pacote de modelos de domínio."""
from src.modelos.pessoa import Pessoa
from src.modelos.registros import Abastecimento, Evento, Manutencao, Viagem
from src.modelos.status import StatusVeiculo
from src.modelos.estrategias import (
    Basica,
    Complexa,
    EstrategiaCustoManutencao,
    Pesada,
    obter_estrategia,
)
from src.modelos.mixins import AbastecivelMixin, ManutenivelMixin
from src.modelos.motorista import Motorista
from src.modelos.veiculo import Caminhao, Carro, Moto, Veiculo, criar_veiculo

__all__ = [
    "Pessoa", "Motorista", "Veiculo", "Carro", "Moto", "Caminhao", "criar_veiculo",
    "AbastecivelMixin", "ManutenivelMixin", "Manutencao", "Abastecimento",
    "Viagem", "Evento", "StatusVeiculo", "EstrategiaCustoManutencao",
    "Basica", "Complexa", "Pesada", "obter_estrategia",
]