"""Módulo contendo os mixins para herança múltipla em Veiculo."""


class AbastecivelMixin:
    """Mixin que adiciona capacidades de gerenciamento de abastecimento."""

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
        pass


class ManutenivelMixin:
    """Mixin que adiciona capacidades de controle de manutenção e status."""

    def registrar_manutencao(self, manutencao: object) -> None:
        """Adiciona um registro de manutenção ao histórico do veículo.

        Args:
            manutencao (object): Objeto de manutenção contendo os detalhes.
        """
        pass

    def alterar_status(self, novo_status: str) -> None:
        """Altera o status do veículo (ATIVO, MANUTENCAO, INATIVO).

        Args:
            novo_status (str): Novo estado do veículo.
        """
        pass