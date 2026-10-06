"""Pacote de modelos do sistema de gerenciamento de frota."""

from src.modelos.pessoa import Pessoa
from src.modelos.motorista import Motorista
from src.modelos.registros import Viagem, Manutencao, Abastecimento
from src.modelos.mixins import AbastecivelMixin, ManutenivelMixin
from src.modelos.veiculo import Veiculo, Carro, Moto, Caminhao

__all__ = [
    "Pessoa",
    "Motorista",
    "Viagem",
    "Manutencao",
    "Abastecimento",
    "AbastecivelMixin",
    "ManutenivelMixin",
    "Veiculo",
    "Carro",
    "Moto",
    "Caminhao",
]