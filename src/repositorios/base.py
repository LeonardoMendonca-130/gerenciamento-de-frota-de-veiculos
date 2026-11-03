"""Contrato comum dos repositórios (padrão Repository)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


def estrutura_vazia() -> dict[str, Any]:
    """Estado inicial de um repositório vazio."""
    return {"veiculos": [], "motoristas": []}


class RepositorioBase(ABC):
    """Interface de persistência, independente do domínio."""

    @abstractmethod
    def ler_dados(self) -> dict[str, Any]:
        """Lê o estado completo. Levanta RepositorioError em caso de falha."""

    @abstractmethod
    def salvar_dados(self, dados: dict[str, Any]) -> None:
        """Grava o estado completo. Levanta RepositorioError em caso de falha."""