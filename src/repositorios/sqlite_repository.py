"""Persistência em SQLite (alternativa ao JsonRepository)."""
from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from typing import Any

from src.excecoes import RepositorioError
from src.repositorios.base import RepositorioBase, estrutura_vazia


class SqliteRepository(RepositorioBase):
    """Guarda o estado da frota (serializado em JSON) em uma tabela SQLite."""

    def __init__(self, caminho: str = "dados_frota.db") -> None:
        self.caminho = caminho
        try:
            with closing(sqlite3.connect(self.caminho)) as conn, conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS estado ("
                    "id INTEGER PRIMARY KEY CHECK (id = 1), dados TEXT NOT NULL)"
                )
        except sqlite3.Error as erro:
            raise RepositorioError(f"Falha ao iniciar SQLite: {erro}") from erro

    def ler_dados(self) -> dict[str, Any]:
        try:
            with closing(sqlite3.connect(self.caminho)) as conn:
                linha = conn.execute("SELECT dados FROM estado WHERE id = 1").fetchone()
            return json.loads(linha[0]) if linha else estrutura_vazia()
        except (sqlite3.Error, json.JSONDecodeError) as erro:
            raise RepositorioError(f"Falha ao ler SQLite: {erro}") from erro

    def salvar_dados(self, dados: dict[str, Any]) -> None:
        try:
            with closing(sqlite3.connect(self.caminho)) as conn, conn:
                conn.execute(
                    "INSERT OR REPLACE INTO estado (id, dados) VALUES (1, ?)",
                    (json.dumps(dados, ensure_ascii=False),),
                )
        except (sqlite3.Error, TypeError) as erro:
            raise RepositorioError(f"Falha ao gravar SQLite: {erro}") from erro