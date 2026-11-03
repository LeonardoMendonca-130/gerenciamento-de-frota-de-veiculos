"""Persistência em arquivo JSON."""
from __future__ import annotations

import json
import os
from typing import Any

from src.excecoes import RepositorioError
from src.repositorios.base import RepositorioBase, estrutura_vazia


class JsonRepository(RepositorioBase):
    """Lê e grava o estado da frota em um arquivo JSON."""

    def __init__(self, caminho_ficheiro: str = "dados_frota.json") -> None:
        self.caminho_ficheiro = caminho_ficheiro
        if not os.path.exists(self.caminho_ficheiro):
            self.salvar_dados(estrutura_vazia())

    def salvar_dados(self, dados: dict[str, Any]) -> None:
        """Escreve o dicionário com json.dump (gravação atômica)."""
        temporario = f"{self.caminho_ficheiro}.tmp"
        try:
            with open(temporario, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            os.replace(temporario, self.caminho_ficheiro)
        except (OSError, TypeError) as erro:
            raise RepositorioError(f"Falha ao gravar JSON: {erro}") from erro

    def ler_dados(self) -> dict[str, Any]:
        """Lê o arquivo com json.load."""
        try:
            with open(self.caminho_ficheiro, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as erro:
            raise RepositorioError(f"Falha ao ler JSON: {erro}") from erro