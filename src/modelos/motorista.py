"""Módulo contendo a classe Motorista."""

from src.modelos.pessoa import Pessoa


class Motorista(Pessoa):
    """Representa um motorista cadastrado no sistema.

    Attributes:
        cnh_categoria (str): Categoria da CNH (ex: 'A', 'B', 'C').
        tempo_experiencia_anos (int): Anos de experiência do motorista.
        disponivel (bool): Indica se o motorista está disponível para viagens.
    """

    def __init__(
        self,
        nome: str,
        cpf: str,
        cnh_categoria: str,
        tempo_experiencia_anos: int,
    ) -> None:
        """Inicializa um motorista."""
        pass

    def registrar_viagem(self, viagem: object) -> None:
        """Registra uma viagem realizada pelo motorista.

        Args:
            viagem (object): Objeto do tipo Viagem.
        """
        pass