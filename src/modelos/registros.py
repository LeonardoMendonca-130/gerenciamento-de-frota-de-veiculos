"""Registros auxiliares: Manutencao, Abastecimento, Viagem e Evento."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from src.excecoes import ManutencaoInvalidaError

TIPOS_MANUTENCAO = frozenset({"preventiva", "corretiva"})


def agora() -> str:
    """Data/hora atual em formato ISO (segundos)."""
    return datetime.now().isoformat(timespec="seconds")


class Manutencao:
    """Registra informações de uma manutenção efetuada."""

    def __init__(self, data: str, tipo: str, custo: float, descricao: str) -> None:
        """Inicializa o registro de manutenção.

        Args:
            data (str): Data do serviço.
            tipo (str): 'preventiva' ou 'corretiva'.
            custo (float): Custo total (>= 0).
            descricao (str): Descrição do serviço.

        Raises:
            ManutencaoInvalidaError: Se o tipo for inválido ou o custo negativo.
        """
        tipo_norm = tipo.strip().lower()
        if tipo_norm not in TIPOS_MANUTENCAO:
            raise ManutencaoInvalidaError(
                f"Tipo de manutenção inválido: '{tipo}'. Use 'preventiva' ou 'corretiva'."
            )
        if custo < 0:
            raise ManutencaoInvalidaError("O custo da manutenção não pode ser negativo.")
        self.data = data
        self.tipo = tipo_norm
        self.custo = float(custo)
        self.descricao = descricao

    def para_dict(self) -> dict[str, Any]:
        """Serializa o registro."""
        return {"data": self.data, "tipo": self.tipo,
                "custo": self.custo, "descricao": self.descricao}

    @classmethod
    def de_dict(cls, d: dict[str, Any]) -> "Manutencao":
        """Reconstrói o registro a partir de um dicionário."""
        return cls(d["data"], d["tipo"], d["custo"], d["descricao"])

    def __str__(self) -> str:
        return f"Manutenção [{self.tipo.upper()}] em {self.data} - R$ {self.custo:.2f}"


class Abastecimento:
    """Registra informações de um abastecimento efetuado."""

    def __init__(
        self, data: str, tipo_combustivel: str, litros: float, valor: float
    ) -> None:
        """Inicializa o registro de abastecimento.

        Raises:
            ValueError: Se litros ou valor não forem positivos.
        """
        if litros <= 0 or valor <= 0:
            raise ValueError("Litros e valor devem ser maiores que zero.")
        self.data = data
        self.tipo_combustivel = tipo_combustivel
        self.litros = float(litros)
        self.valor = float(valor)

    def para_dict(self) -> dict[str, Any]:
        """Serializa o registro."""
        return {"data": self.data, "tipo_combustivel": self.tipo_combustivel,
                "litros": self.litros, "valor": self.valor}

    @classmethod
    def de_dict(cls, d: dict[str, Any]) -> "Abastecimento":
        """Reconstrói o registro a partir de um dicionário."""
        return cls(d["data"], d["tipo_combustivel"], d["litros"], d["valor"])

    def __str__(self) -> str:
        return (f"Abastecimento em {self.data}: {self.litros}L "
                f"({self.tipo_combustivel}) - R$ {self.valor:.2f}")


class Viagem:
    """Registra informações de uma viagem realizada por um motorista."""

    def __init__(
        self, origem: str, destino: str, distancia_percorrida: float, placa: str = ""
    ) -> None:
        """Inicializa o registro de viagem.

        Raises:
            ValueError: Se a distância não for positiva.
        """
        if distancia_percorrida <= 0:
            raise ValueError("A distância percorrida deve ser maior que zero.")
        self.origem = origem
        self.destino = destino
        self.distancia_percorrida = float(distancia_percorrida)
        self.placa = placa

    def para_dict(self) -> dict[str, Any]:
        """Serializa o registro."""
        return {"origem": self.origem, "destino": self.destino,
                "distancia": self.distancia_percorrida, "placa": self.placa}

    @classmethod
    def de_dict(cls, d: dict[str, Any]) -> "Viagem":
        """Reconstrói o registro a partir de um dicionário."""
        return cls(d["origem"], d["destino"], d["distancia"], d.get("placa", ""))

    def __str__(self) -> str:
        return f"Viagem: {self.origem} -> {self.destino} ({self.distancia_percorrida} km)"


class Evento:
    """Evento do histórico do veículo (entrada, saída, manutenção...)."""

    def __init__(self, tipo: str, descricao: str, data: str | None = None) -> None:
        self.tipo = tipo
        self.descricao = descricao
        self.data = data or agora()

    def para_dict(self) -> dict[str, Any]:
        """Serializa o evento."""
        return {"data": self.data, "tipo": self.tipo, "descricao": self.descricao}

    @classmethod
    def de_dict(cls, d: dict[str, Any]) -> "Evento":
        """Reconstrói o evento a partir de um dicionário."""
        return cls(d["tipo"], d["descricao"], d["data"])

    def __str__(self) -> str:
        return f"[{self.data}] {self.tipo.upper()}: {self.descricao}"