"""Módulo contendo a classe Pessoa."""


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
        """
        if not nome.strip():
            raise ValueError("O nome não pode ser vazio.")
        if not cpf.strip():
            raise ValueError("O CPF não pode ser vazio.")

        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self) -> str:
        """Retorna o nome da pessoa."""
        return self._nome

    @property
    def cpf(self) -> str:
        """Retorna o CPF da pessoa."""
        return self._cpf
