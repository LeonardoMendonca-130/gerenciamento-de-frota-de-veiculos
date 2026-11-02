"""Estados possíveis de um veículo ."""
from __future__ import annotations

from enum import Enum


class StatusVeiculo(str, Enum):
    """ATIVO -> MANUTENCAO -> ATIVO; ATIVO -> INATIVO."""

    ATIVO = "ATIVO"
    MANUTENCAO = "MANUTENCAO"
    INATIVO = "INATIVO"

    @classmethod
    def de_texto(cls, texto: str) -> "StatusVeiculo":
        """Converte texto (case-insensitive) em status, ou levanta ValueError."""
        try:
            return cls(str(texto).strip().upper())
        except ValueError:
            validos = ", ".join(s.value for s in cls)
            raise ValueError(
                f"Status inválido: '{texto}'. Opções válidas: {validos}"
            ) from None

    def pode_ir_para(self, novo: "StatusVeiculo") -> bool:
        """Indica se a transição self -> novo é permitida."""
        return novo in _TRANSICOES[self]


_TRANSICOES: dict[StatusVeiculo, set[StatusVeiculo]] = {
    StatusVeiculo.ATIVO: {StatusVeiculo.MANUTENCAO, StatusVeiculo.INATIVO},
    StatusVeiculo.MANUTENCAO: {StatusVeiculo.ATIVO},
    StatusVeiculo.INATIVO: set(),
}