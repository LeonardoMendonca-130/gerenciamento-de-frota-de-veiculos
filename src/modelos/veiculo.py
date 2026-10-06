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
        if not placa.strip():
            raise ValueError("A placa não pode ser vazia.")
            
        self._placa = placa.strip().upper()
        self._marca = marca.strip()
        self._modelo = modelo.strip()
        self._ano = int(ano)
        
        # Chama construtores dos Mixins para inicializar listas de histórico
        super().__init__()
        
        self.quilometragem = quilometragem  # Valida via setter (>= 0)
        self.consumo_medio = consumo_medio  # Valida via setter (> 0)
        self._status = "ATIVO"
        
    @property
    def placa(self) -> str:
        return self._placa
        
    @property
    def marca(self) -> str:
        return self._marca
        
    @property
    def modelo(self) -> str:
        return self._modelo
        
    @property
    def ano(self) -> int:
        return self._ano
        
    @property
    def quilometragem(self) -> float:
        return self._quilometragem
        
    @quilometragem.setter
    def quilometragem(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("A quilometragem não pode ser negativa.")
        self._quilometragem = float(valor)

    @property
    def consumo_medio(self) -> float:
        return self._consumo_medio
        
    @consumo_medio.setter
    def consumo_medio(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O consumo médio deve ser maior que zero.")
        self._consumo_medio = float(valor)
        
    @property
    def status(self) -> str:
        return self._status
        
    @status.setter
    def status(self, novo_status: str) -> None:
        status_upper = novo_status.strip().upper()
        if status_upper not in self.STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido: '{novo_status}'. Válidos: {self.STATUS_VALIDOS}"
            )
        self._status = status_upper
        
        
    # --- MÉTODOS ESPECIAIS REQUISITADOS ---
    
    def __str__(self) -> str:
        """Retorna representação legível do veículo em string."""
        return (
            f"{self.__class__.__name__} {self.modelo} ({self.marca}) "
            f"- Placa: {self.placa} | KM: {self.quilometragem} | Status: {self.status}"
        )

    def __repr__(self) -> str:
        """Retorna representação oficial do objeto para depuração."""
        return (
            f"{self.__class__.__name__}(placa='{self.placa}', "
            f"marca='{self.marca}', modelo='{self.modelo}', ano={self.ano})"
        )

    def __eq__(self, other: object) -> bool:
        """Compara dois veículos pela placa."""
        if not isinstance(other, Veiculo):
            return False
        return self.placa == other.placa

    def __lt__(self, other: "Veiculo") -> bool:
        """Compara dois veículos pela quilometragem."""
        if not isinstance(other, Veiculo):
            return NotImplemented
        return self.quilometragem < other.quilometragem
    
    def __iter__(self):
        """Permite iterar sobre o histórico de manutenções do veículo."""
        return iter(self.historico_manutencoes)

class Carro(Veiculo):
    """Representa um veículo do tipo Carro (requer CNH B)."""

    pass


class Moto(Veiculo):
    """Representa um veículo do tipo Moto (requer CNH A)."""

    pass


class Caminhao(Veiculo):
    """Representa um veículo do tipo Caminhão (requer CNH C ou superior)."""

    pass