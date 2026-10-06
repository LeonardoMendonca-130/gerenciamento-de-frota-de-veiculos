"""Módulo contendo os mixins para herança múltipla em Veiculo."""

from src.modelos.registros import Abastecimento, Manutencao

class AbastecivelMixin:
    """Mixin que adiciona capacidades de gerenciamento de abastecimento."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._historico_abastecimentos: list[Abastecimento] = []
        
    @property
    def historico_abastecimentos(self) -> list[Abastecimento]:
        return list(self._historico_abastecimentos)

    def abastecer(
        self, data: str, tipo_combustivel: str, litros: float, valor: float
    ) -> None:
        """Registra um abastecimento no veículo.

        Args:
            data (str): Data do abastecimento.
            tipo_combustivel (str): Tipo de combustível utilizado.
            litros (float): Quantidade de litros abastecidos.
            valor (float): Valor total pago.
        """
        
        novo_abastecimento = Abastecimento(data, tipo_combustivel, litros, valor)
        self._historico_abastecimentos.append(novo_abastecimento)


class ManutenivelMixin:
    """Mixin que adiciona capacidades de controle de manutenção e status."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._historico_manutencoes: list[Manutencao] = []
        
    @property
    def historico_manutencoes(self) -> list[Manutencao]:
        return list(self._historico_manutencoes)
        
    def registrar_manutencao(self, manutencao: object) -> None:
        """Adiciona um registro de manutenção ao histórico do veículo.

        Args:
            manutencao (object): Objeto de manutenção contendo os detalhes.
        """
        if not isinstance(manutencao, Manutencao):
            raise TypeError("O registro deve ser um objeto do tipo Manutencao.")
        self._historico_manutencoes.append(manutencao)

    def alterar_status(self, novo_status: str) -> None:
        """Altera o status do veículo (ATIVO, MANUTENCAO, INATIVO).

        Args:
            novo_status (str): Novo estado do veículo.
            
        Raises:
            ValueError: Se o status informado for inválido.
        """
        
        status_upper = novo_status.strip().upper()
        if status_upper not in self.STATUS_VALIDOS:
            raise ValueError(
                f"Status inválido: '{novo_status}'. Opções válidas: {self.STATUS_VALIDOS}"
            )
        self._status = status_upper