"""Módulo para registros auxiliares: Manutencao, Abastecimento e Viagem."""


class Manutencao:
    """Registra informações de uma manutenção efetuada."""

    def __init__(
        self, data: str, tipo: str, custo: float, descricao: str
    ) -> None:
        """Inicializa o registro de manutenção."""
        
        if custo < 0:
            raise ValueError("O custo da manutenção não pode ser negativo.")
        self.data = data
        self.tipo = tipo  # ex: 'preventiva' ou 'corretiva'
        self.custo = float(custo)
        self.descricao = descricao
        
    def __str__(self) -> str:
        return f"Manutenção [{self.tipo.upper()}] em {self.data} - R$ {self.custo:.2f}"


class Abastecimento:
    """Registra informações de um abastecimento efetuado."""

    def __init__(
        self, data: str, tipo_combustivel: str, litros: float, valor: float
    ) -> None:
        """Inicializa o registro de abastecimento."""
        
        if litros <= 0 or valor <= 0:
            raise ValueError("Litros e valor devem ser maiores que zero.")
            
        self.data = data
        self.tipo_combustivel = tipo_combustivel
        self.litros = float(litros)
        self.valor = float(valor)

    def __str__(self) -> str:
        return f"Abastecimento em {self.data}: {self.litros}L ({self.tipo_combustivel}) - R$ {self.valor:.2f}"


class Viagem:
    """Registra informações de uma viagem realizada por um motorista."""

    def __init__(
        self, origem: str, destino: str, distancia_percorrida: float
    ) -> None:
        """Inicializa o registro de viagem."""
        
        if distancia_percorrida <= 0:
            raise ValueError(
                "A distância percorrida deve ser maior que zero."
            )
        
        self.origem = origem
        self.destino = destino
        self.distancia_percorrida = float(distancia_percorrida)
        
    def __str__(self) -> str:
        return f"Viagem: {self.origem} -> {self.destino} ({self.distancia_percorrida} km)"