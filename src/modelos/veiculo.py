"""Módulo contendo a hierarquia de veículos."""

from src.modelos.mixins import AbastecivelMixin, ManutenivelMixin


class Veiculo(AbastecivelMixin, ManutenivelMixin):
    """Classe base que representa um veículo genérico da frota.

    Attributes:
        placa (str): Placa do veículo.
        marca (str): Marca do veículo.
        modelo (str): Modelo do veículo.
        ano (int): Ano de fabricação.
        quilometragem (float): Quilometragem atual rodada.
        consumo_medio (float): Consumo médio em km/l.
        status (str): Status atual do veículo.
    """

    def __init__(
        self,
        placa: str,
        marca: str,
        modelo: str,
        ano: int,
        quilometragem: float,
        consumo_medio: float,
    ) -> None:
        """Inicializa os dados básicos do veículo."""
        pass

    def __str__(self) -> str:
        """Retorna representação legível do veículo em string."""
        pass

    def __repr__(self) -> str:
        """Retorna representação oficial do objeto para depuração."""
        pass

    def __eq__(self, other: object) -> bool:
        """Compara dois veículos pela placa."""
        pass

    def __lt__(self, other: "Veiculo") -> bool:
        """Compara dois veículos pela quilometragem."""
        pass


class Carro(Veiculo):
    """Representa um veículo do tipo Carro (requer CNH B)."""

    pass


class Moto(Veiculo):
    """Representa um veículo do tipo Moto (requer CNH A)."""

    pass


class Caminhao(Veiculo):
    """Representa um veículo do tipo Caminhão (requer CNH C ou superior)."""

    pass