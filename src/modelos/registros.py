"""Módulo para registros auxiliares: Manutencao, Abastecimento e Viagem."""


class Manutencao:
    """Registra informações de uma manutenção efetuada."""

    def __init__(
        self, data: str, tipo: str, custo: float, descricao: str
    ) -> None:
        """Inicializa o registro de manutenção."""
        pass


class Abastecimento:
    """Registra informações de um abastecimento efetuado."""

    def __init__(
        self, data: str, tipo_combustivel: str, litros: float, valor: float
    ) -> None:
        """Inicializa o registro de abastecimento."""
        pass


class Viagem:
    """Registra informações de uma viagem realizada por um motorista."""

    def __init__(
        self, origem: str, destino: str, distancia_percorrida: float
    ) -> None:
        """Inicializa o registro de viagem."""
        pass