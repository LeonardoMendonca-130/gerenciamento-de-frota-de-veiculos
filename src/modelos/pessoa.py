"""Módulo contendo a classe Pessoa."""
from __future__ import annotations

class Pessoa:
    """Representa uma pessoa no sistema.

    Attributes:
        nome (str): Nome completo da pessoa.
        cpf (str): CPF da pessoa.
    """

    def __init__(self, nome: str, cpf: str) -> None:
        """Inicializa uma nova instância de Pessoa.

        Args:
            nome (str): Nome da pessoa.
            cpf (str): Número do CPF.

        Raises:
            ValueError: Se nome ou CPF forem vazios.
        """
        if not cpf.strip():
            raise ValueError("O CPF não pode ser vazio.")

        self.nome = nome
        self._cpf = cpf.strip()

    @property
    def nome(self) -> str:
        """Retorna o nome da pessoa."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("O nome não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def cpf(self) -> str:
        """Retorna o CPF da pessoa."""
        return self._cpf

    def __str__(self) -> str:
        return f"{self.nome} (CPF: {self.cpf})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nome='{self.nome}', cpf='{self.cpf}')"