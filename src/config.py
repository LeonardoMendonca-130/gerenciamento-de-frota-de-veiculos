"""Carregamento das regras de negócio configuráveis (settings.json)."""
from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

CAMINHO_PADRAO = Path(__file__).resolve().parent / "settings.json"

PADRAO: dict[str, Any] = {
    "limite_km_revisao_preventiva": 10000,
    "faixa_consumo_aceitavel": {"minimo": 8, "maximo": 20},
    "faixa_consumo_por_tipo": {},
    "custos_manutencao": {"basica": 150.0, "complexa": 400.0, "pesada": 900.0},
    "categorias_cnh_minimas": {"Moto": "A", "Carro": "B", "Caminhao": "C"},
}


class Settings:
    """Políticas e parâmetros do sistema, lidos do settings.json."""

    def __init__(self, dados: dict[str, Any] | None = None) -> None:
        self._dados: dict[str, Any] = copy.deepcopy(PADRAO)
        self._dados.update(copy.deepcopy(dados or {}))

    @classmethod
    def carregar(cls, caminho: str | Path | None = None) -> "Settings":
        """Lê o arquivo JSON; se não existir, usa os valores padrão."""
        arquivo = Path(caminho) if caminho else CAMINHO_PADRAO
        if not arquivo.exists():
            return cls()
        try:
            with open(arquivo, encoding="utf-8") as f:
                return cls(json.load(f))
        except (OSError, json.JSONDecodeError) as erro:
            raise ValueError(f"settings.json inválido: {erro}") from erro

    @property
    def limite_km_revisao(self) -> float:
        """Quilometragem entre revisões preventivas."""
        return float(self._dados["limite_km_revisao_preventiva"])

    def faixa_consumo(self, tipo: str | None = None) -> tuple[float, float]:
        """Faixa aceitável (mínimo, máximo) de km/l, global ou por tipo."""
        faixa = self._dados["faixa_consumo_aceitavel"]
        faixa = self._dados.get("faixa_consumo_por_tipo", {}).get(tipo, faixa)
        return float(faixa["minimo"]), float(faixa["maximo"])

    def custo_base_manutencao(self, nome_estrategia: str) -> float:
        """Custo base configurado para a estratégia (basica/complexa/pesada)."""
        return float(self._dados["custos_manutencao"][nome_estrategia])

    def cnhs_permitidas(self, tipo: str) -> frozenset[str]:
        """Categorias de CNH aceitas para o tipo de veículo.

        Moto exige 'A'. Para os demais, vale a categoria mínima ou superior
        (B < C < D < E).
        """
        minima = str(self._dados["categorias_cnh_minimas"][tipo]).upper()
        if minima == "A":
            return frozenset({"A"})
        return frozenset(c for c in "BCDE" if c >= minima)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Retorna a instância única de configurações do sistema."""
    return Settings.carregar()