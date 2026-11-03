"""Módulo contendo a classe Motorista."""
from __future__ import annotations

from typing import Any

from src.modelos.pessoa import Pessoa
from src.modelos.registros import Viagem


class Motorista(Pessoa):
    """Representa um motorista cadastrado no sistema.

    Attributes:
        cnh_categoria (str): Categoria da CNH (A a E).
        tempo_experiencia_anos (int): Anos de experiência.
        disponivel (bool): Se está disponível para viagens.
    """

    CATEGORIAS_VALIDAS = frozenset({"A", "B", "C", "D", "E"})

    def __init__(
        self, nome: str, cpf: str, cnh_categoria: str, tempo_experiencia_anos: int
    ) -> None:
        """Inicializa um motorista (valida CNH e experiência via setters)."""
        super().__init__(nome, cpf)
        self.cnh_categoria = cnh_categoria
        self.tempo_experiencia_anos = tempo_experiencia_anos
        self._disponivel = True
        self._historico_viagens: list[Viagem] = []

    @property
    def cnh_categoria(self) -> str:
        return self._cnh_categoria

    @cnh_categoria.setter
    def cnh_categoria(self, valor: str) -> None:
        categoria = valor.strip().upper()
        if categoria not in self.CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Categoria CNH inválida: '{valor}'. "
                f"Válidas: {sorted(self.CATEGORIAS_VALIDAS)}"
            )
        self._cnh_categoria = categoria

    @property
    def tempo_experiencia_anos(self) -> int:
        return self._tempo_experiencia_anos

    @tempo_experiencia_anos.setter
    def tempo_experiencia_anos(self, valor: int) -> None:
        if valor < 0:
            raise ValueError("O tempo de experiência não pode ser negativo.")
        self._tempo_experiencia_anos = int(valor)

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    @disponivel.setter
    def disponivel(self, status: bool) -> None:
        self._disponivel = bool(status)

    @property
    def historico_viagens(self) -> list[Viagem]:
        """Cópia da lista com o histórico de viagens."""
        return list(self._historico_viagens)

    @property
    def total_viagens(self) -> int:
        """Quantidade de viagens realizadas."""
        return len(self._historico_viagens)

    @property
    def km_total(self) -> float:
        """Distância total percorrida em todas as viagens."""
        return sum(v.distancia_percorrida for v in self._historico_viagens)

    def registrar_viagem(self, viagem: Viagem) -> None:
        """Registra uma viagem realizada pelo motorista.

        Raises:
            TypeError: Se o objeto não for uma Viagem.
        """
        if not isinstance(viagem, Viagem):
            raise TypeError("O objeto fornecido deve ser uma instância de Viagem.")
        self._historico_viagens.append(viagem)

    def para_dict(self) -> dict[str, Any]:
        """Serializa o motorista."""
        return {
            "nome": self.nome, "cpf": self.cpf,
            "cnh_categoria": self.cnh_categoria,
            "tempo_experiencia_anos": self.tempo_experiencia_anos,
            "disponivel": self.disponivel,
            "viagens": [v.para_dict() for v in self._historico_viagens],
        }

    @classmethod
    def de_dict(cls, d: dict[str, Any]) -> "Motorista":
        """Reconstrói o motorista a partir de um dicionário."""
        m = cls(d["nome"], d["cpf"], d["cnh_categoria"], d["tempo_experiencia_anos"])
        m._disponivel = bool(d.get("disponivel", True))
        m._historico_viagens = [Viagem.de_dict(v) for v in d.get("viagens", [])]
        return m

    def __str__(self) -> str:
        status_str = "Livre" if self.disponivel else "Em Viagem"
        return (
            f"Motorista: {self.nome} | CNH: {self.cnh_categoria} | "
            f"Exp: {self.tempo_experiencia_anos} anos | Status: {status_str}"
        )