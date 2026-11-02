"""Estratégia adotada para o cálculo do custo de manutenção."""
from __future__ import annotations

from abc import ABC, abstractmethod


class EstrategiaCustoManutencao(ABC):
    """Interface das estratégias de cálculo de custo."""

    nome: str = ""

    @abstractmethod
    def calcular(self, custo_base: float, custo_pecas: float = 0.0) -> float:
        """Calcula o custo final a partir do custo base e do custo de peças."""


class Basica(EstrategiaCustoManutencao):
    """Serviço simples: base + peças."""

    nome = "basica"

    def calcular(self, custo_base: float, custo_pecas: float = 0.0) -> float:
        return round(custo_base + custo_pecas, 2)


class Complexa(EstrategiaCustoManutencao):
    """Serviço complexo: peças especializadas com acréscimo de 20%."""

    nome = "complexa"

    def calcular(self, custo_base: float, custo_pecas: float = 0.0) -> float:
        return round(custo_base + custo_pecas * 1.2, 2)


class Pesada(EstrategiaCustoManutencao):
    """Serviço pesado: acréscimo de 50% sobre base + peças."""

    nome = "pesada"

    def calcular(self, custo_base: float, custo_pecas: float = 0.0) -> float:
        return round((custo_base + custo_pecas) * 1.5, 2)


ESTRATEGIAS: dict[str, EstrategiaCustoManutencao] = {
    e.nome: e for e in (Basica(), Complexa(), Pesada())
}


def obter_estrategia(nome: str) -> EstrategiaCustoManutencao:
    """Retorna a estratégia pelo nome ou levanta ValueError."""
    try:
        return ESTRATEGIAS[nome.strip().lower()]
    except KeyError:
        raise ValueError(
            f"Estratégia inválida: '{nome}'. Opções: {', '.join(ESTRATEGIAS)}."
        ) from None