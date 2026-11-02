"""Módulo contendo os mixins para herança múltipla em Veiculo."""
from __future__ import annotations

from src.excecoes import ManutencaoInvalidaError
from src.modelos.registros import Abastecimento, Manutencao
from src.modelos.status import StatusVeiculo


class AbastecivelMixin:
    """Mixin que adiciona capacidades de gerenciamento de abastecimento."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._historico_abastecimentos: list[Abastecimento] = []

    @property
    def historico_abastecimentos(self) -> list[Abastecimento]:
        """Cópia do histórico de abastecimentos."""
        return list(self._historico_abastecimentos)

    @property
    def litros_totais(self) -> float:
        """Total de litros abastecidos."""
        return sum(a.litros for a in self._historico_abastecimentos)

    @property
    def gasto_total_combustivel(self) -> float:
        """Total pago em abastecimentos."""
        return sum(a.valor for a in self._historico_abastecimentos)

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
        self._historico_abastecimentos.append(
            Abastecimento(data, tipo_combustivel, litros, valor)
        )


class ManutenivelMixin:
    """Mixin que adiciona controle de manutenção e de status (State)."""

    STATUS_VALIDOS = frozenset(s.value for s in StatusVeiculo)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._historico_manutencoes: list[Manutencao] = []
        self._status: StatusVeiculo = StatusVeiculo.ATIVO

    @property
    def status(self) -> str:
        """Status atual (ATIVO, MANUTENCAO ou INATIVO)."""
        return self._status.value

    @property
    def historico_manutencoes(self) -> list[Manutencao]:
        """Cópia do histórico de manutenções."""
        return list(self._historico_manutencoes)

    def registrar_manutencao(self, manutencao: Manutencao) -> None:
        """Adiciona um registro de manutenção ao histórico do veículo.

        Raises:
            TypeError: Se o objeto não for uma Manutencao.
        """
        if not isinstance(manutencao, Manutencao):
            raise TypeError("O registro deve ser um objeto do tipo Manutencao.")
        self._historico_manutencoes.append(manutencao)

    def alterar_status(self, novo_status: str) -> None:
        """Altera o status respeitando as transições permitidas.

        Raises:
            ValueError: Se o status for desconhecido.
            ManutencaoInvalidaError: Se a transição não for permitida.
        """
        novo = StatusVeiculo.de_texto(novo_status)
        if not self._status.pode_ir_para(novo):
            raise ManutencaoInvalidaError(
                f"Transição inválida: {self._status.value} -> {novo.value}."
            )
        self._status = novo

    def enviar_para_manutencao(self, manutencao: Manutencao) -> None:
        """Muda o status para MANUTENCAO e registra a manutenção."""
        if not isinstance(manutencao, Manutencao):
            raise TypeError("O registro deve ser um objeto do tipo Manutencao.")
        self.alterar_status("MANUTENCAO")
        self.registrar_manutencao(manutencao)

    def concluir_manutencao(self) -> None:
        """Libera o veículo após a manutenção (volta a ATIVO)."""
        if self._status is not StatusVeiculo.MANUTENCAO:
            raise ManutencaoInvalidaError("O veículo não está em manutenção.")
        self.alterar_status("ATIVO")