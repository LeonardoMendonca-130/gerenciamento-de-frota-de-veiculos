"""Módulo contendo a classe Motorista."""

from src.modelos.pessoa import Pessoa
from src.modelos.registros import Viagem

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
        
        super().__init__(nome, cpf)
        self.cnh_categoria = cnh_categoria  # Valida via setter
        self.tempo_experiencia_anos = tempo_experiencia_anos  # Valida via setter
        self._disponivel = True
        self._historico_viagens: list[Viagem] = []
      
    @property
    def cnh_categoria(self) -> str:
        return self._cnh_categoria

    @cnh_categoria.setter
    def cnh_categoria(self, valor: str) -> None:
        categoria_upper = valor.strip().upper()
        if categoria_upper not in self.CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Categoria CNH inválida: '{valor}'. Válidas: {self.CATEGORIAS_VALIDAS}"
            )
        self._cnh_categoria = categoria_upper

    @property
    def tempo_experiencia_anos(self) -> int:
        return self._tempo_experiencia_anos

    @tempo_experiencia_anos.setter
    def tempo_experiencia_anos(self, valor: int) -> None:
        if valor < 0:
            raise ValueError(
                "O tempo de experiência não pode ser negativo."
            )
        self._tempo_experiencia_anos = int(valor)

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    @disponivel.setter
    def disponivel(self, status: bool) -> None:
        self._disponivel = bool(status)

    @property
    def historico_viagens(self) -> list[Viagem]:
        """Retorna uma cópia da lista com o histórico de viagens do motorista."""
        return list(self._historico_viagens)

    def registrar_viagem(self, viagem: object) -> None:
        """Registra uma viagem realizada pelo motorista.

        Args:
            viagem (object): Objeto do tipo Viagem.
        """
        
        if not isinstance(viagem, Viagem):
            raise TypeError("O objeto fornecido deve ser uma instância de Viagem.")
        self._historico_viagens.append(viagem)

    def __str__(self) -> str:
        status_str = "Livre" if self.disponivel else "Em Viagem"
        return (
            f"Motorista: {self.nome} | CNH: {self.cnh_categoria} | "
            f"Exp: {self.tempo_experiencia_anos} anos | Status: {status_str}"
        )