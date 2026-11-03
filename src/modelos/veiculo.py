"""Módulo contendo a hierarquia de veículos."""
from __future__ import annotations

from datetime import date
from typing import Any

from src.config import Settings, get_settings
from src.excecoes import (
    AlocacaoInvalidaError,
    ManutencaoInvalidaError,
    PoliticaNaoAtendidaError,
)
from src.modelos.mixins import AbastecivelMixin, ManutenivelMixin
from src.modelos.motorista import Motorista
from src.modelos.registros import Abastecimento, Evento, Manutencao, Viagem
from src.modelos.status import StatusVeiculo


class Veiculo(AbastecivelMixin, ManutenivelMixin):
    """Classe base (abstrata) que representa um veículo da frota.

    Attributes:
        placa (str): Placa do veículo.
        marca (str): Marca do veículo.
        modelo (str): Modelo do veículo.
        ano (int): Ano de fabricação.
        quilometragem (float): Quilometragem atual.
        consumo_medio (float): Consumo médio declarado (km/l).
        status (str): Status atual (somente leitura; use alterar_status).
    """

    TIPO: str = "Veiculo"

    def __init__(
        self,
        placa: str,
        marca: str,
        modelo: str,
        ano: int,
        quilometragem: float,
        consumo_medio: float,
        *,
        settings: Settings | None = None,
    ) -> None:
        """Inicializa os dados básicos do veículo."""
        if type(self) is Veiculo:
            raise TypeError("Veiculo é abstrata; use Carro, Moto ou Caminhao.")
        if not placa.strip():
            raise ValueError("A placa não pode ser vazia.")
        self._placa = placa.strip().upper()

        super().__init__()  # inicializa históricos e status dos mixins

        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.quilometragem = quilometragem
        self.consumo_medio = consumo_medio

        self._settings = settings or get_settings()
        self._km_inicial: float = self.quilometragem
        self._km_ultima_revisao: float = self.quilometragem
        self._eventos: list[Evento] = []
        self.motorista_alocado: Motorista | None = None

    # --- Propriedades (encapsulamento) ---
    @property
    def placa(self) -> str:
        return self._placa

    @property
    def marca(self) -> str:
        return self._marca

    @marca.setter
    def marca(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("A marca não pode ser vazia.")
        self._marca = valor.strip()

    @property
    def modelo(self) -> str:
        return self._modelo

    @modelo.setter
    def modelo(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("O modelo não pode ser vazio.")
        self._modelo = valor.strip()

    @property
    def ano(self) -> int:
        return self._ano

    @ano.setter
    def ano(self, valor: int) -> None:
        valor = int(valor)
        if not 1900 <= valor <= date.today().year + 1:
            raise ValueError(f"Ano inválido: {valor}.")
        self._ano = valor

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
    def historico_eventos(self) -> list[Evento]:
        """Cópia do histórico de eventos (entrada, saída, manutenção...)."""
        return list(self._eventos)

    # --- Políticas configuráveis ---
    @property
    def cnhs_permitidas(self) -> frozenset[str]:
        """Categorias de CNH aceitas (derivadas do settings.json)."""
        return self._settings.cnhs_permitidas(self.TIPO)

    @property
    def km_desde_revisao(self) -> float:
        """Km rodados desde a última revisão preventiva."""
        return self.quilometragem - self._km_ultima_revisao

    @property
    def revisao_preventiva_pendente(self) -> bool:
        """True se atingiu o limite de km para revisão preventiva."""
        return self.km_desde_revisao >= self._settings.limite_km_revisao

    @property
    def faixa_consumo(self) -> tuple[float, float]:
        """Faixa aceitável de consumo (mín, máx) para este tipo de veículo."""
        return self._settings.faixa_consumo(self.TIPO)

    @property
    def consumo_real(self) -> float | None:
        """Consumo medido (km/l): km rodados no sistema / litros abastecidos."""
        distancia = self.quilometragem - self._km_inicial
        litros = self.litros_totais
        if litros <= 0 or distancia <= 0:
            return None
        return distancia / litros

    @property
    def consumo_efetivo(self) -> float:
        """Consumo medido, ou o declarado quando ainda não há dados medidos."""
        real = self.consumo_real
        return real if real is not None else self.consumo_medio

    @property
    def consumo_fora_da_faixa(self) -> bool:
        """True se o consumo efetivo está fora da faixa aceitável."""
        minimo, maximo = self.faixa_consumo
        return not minimo <= self.consumo_efetivo <= maximo

    # --- Eventos, abastecimento e manutenção ---
    def registrar_evento(self, tipo: str, descricao: str) -> None:
        """Adiciona um evento ao histórico do veículo."""
        self._eventos.append(Evento(tipo, descricao))

    def abastecer(
        self, data: str, tipo_combustivel: str, litros: float, valor: float
    ) -> None:
        """Registra abastecimento e o evento correspondente."""
        super().abastecer(data, tipo_combustivel, litros, valor)
        self.registrar_evento("abastecimento", str(self._historico_abastecimentos[-1]))

    def registrar_manutencao(self, manutencao: Manutencao) -> None:
        """Registra manutenção; se preventiva, zera o contador de revisão."""
        super().registrar_manutencao(manutencao)
        if manutencao.tipo == "preventiva":
            self._km_ultima_revisao = self.quilometragem
        self.registrar_evento("manutencao", str(manutencao))

    def alterar_status(self, novo_status: str) -> None:
        """Altera o status; veículo com motorista alocado não sai de ATIVO."""
        novo = StatusVeiculo.de_texto(novo_status)
        if novo is not StatusVeiculo.ATIVO and self.motorista_alocado is not None:
            raise ManutencaoInvalidaError(
                "Libere o motorista antes de mudar o status do veículo."
            )
        anterior = self.status
        super().alterar_status(novo_status)
        tipo = "desativacao" if novo is StatusVeiculo.INATIVO else "manutencao"
        self.registrar_evento(tipo, f"Status: {anterior} -> {novo.value}")

    # --- Alocação ---
    def alocar_motorista(self, motorista: Motorista) -> None:
        """Associa o veículo a um motorista aplicando as regras de negócio.

        Raises:
            AlocacaoInvalidaError: Veículo não ativo/ocupado ou motorista indisponível.
            PoliticaNaoAtendidaError: Revisão pendente ou CNH incompatível.
        """
        if self.status != "ATIVO":
            raise AlocacaoInvalidaError(
                f"Não é possível alocar. O veículo está {self.status}."
            )
        if self.motorista_alocado is not None:
            raise AlocacaoInvalidaError("O veículo já possui motorista alocado.")
        if self.revisao_preventiva_pendente:
            raise PoliticaNaoAtendidaError(
                f"Revisão preventiva pendente ({self.km_desde_revisao:.0f} km "
                f"desde a última revisão)."
            )
        if motorista.cnh_categoria not in self.cnhs_permitidas:
            raise PoliticaNaoAtendidaError(
                f"CNH '{motorista.cnh_categoria}' incompatível. Este veículo exige "
                f"uma destas categorias: {sorted(self.cnhs_permitidas)}."
            )
        if not motorista.disponivel:
            raise AlocacaoInvalidaError("O motorista não está disponível no momento.")

        self.motorista_alocado = motorista
        motorista.disponivel = False
        self.registrar_evento("saida", f"Alocado ao motorista {motorista.nome}.")

    def desalocar_motorista(self) -> None:
        """Libera o motorista do veículo ao fim do uso."""
        if self.motorista_alocado:
            nome = self.motorista_alocado.nome
            self.motorista_alocado.disponivel = True
            self.motorista_alocado = None
            self.registrar_evento("entrada", f"Devolvido por {nome}.")

    def registrar_viagem(self, origem: str, destino: str, distancia: float) -> Viagem:
        """Registra viagem do motorista alocado e atualiza a quilometragem.

        Raises:
            AlocacaoInvalidaError: Se não houver motorista alocado.
            ValueError: Se a distância for inválida.
        """
        if self.motorista_alocado is None:
            raise AlocacaoInvalidaError("Nenhum motorista alocado a este veículo.")
        viagem = Viagem(origem, destino, distancia, placa=self.placa)
        self.motorista_alocado.registrar_viagem(viagem)
        self.quilometragem = self.quilometragem + viagem.distancia_percorrida
        self.registrar_evento("viagem", str(viagem))
        return viagem

    # --- Persistência ---
    def para_dict(self) -> dict[str, Any]:
        """Serializa o veículo (incluindo históricos)."""
        return {
            "tipo": self.TIPO,
            "placa": self.placa,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "quilometragem": self.quilometragem,
            "consumo_medio": self.consumo_medio,
            "status": self.status,
            "km_inicial": self._km_inicial,
            "km_ultima_revisao": self._km_ultima_revisao,
            "motorista_cpf": self.motorista_alocado.cpf if self.motorista_alocado else None,
            "abastecimentos": [a.para_dict() for a in self._historico_abastecimentos],
            "manutencoes": [m.para_dict() for m in self._historico_manutencoes],
            "eventos": [e.para_dict() for e in self._eventos],
        }

    @staticmethod
    def de_dict(dados: dict[str, Any], settings: Settings | None = None) -> "Veiculo":
        """Reconstrói o veículo (da subclasse correta) a partir de um dicionário.

        O vínculo com o motorista é restabelecido pelo serviço (motorista_cpf).
        """
        classe = classe_por_tipo(dados["tipo"])
        v = classe(
            dados["placa"], dados["marca"], dados["modelo"], dados["ano"],
            dados["quilometragem"], dados["consumo_medio"], settings=settings,
        )
        v._km_inicial = float(dados.get("km_inicial", v.quilometragem))
        v._km_ultima_revisao = float(dados.get("km_ultima_revisao", v.quilometragem))
        v._status = StatusVeiculo.de_texto(dados.get("status", "ATIVO"))
        v._historico_abastecimentos = [
            Abastecimento.de_dict(a) for a in dados.get("abastecimentos", [])
        ]
        v._historico_manutencoes = [
            Manutencao.de_dict(m) for m in dados.get("manutencoes", [])
        ]
        v._eventos = [Evento.de_dict(e) for e in dados.get("eventos", [])]
        return v

    # --- Métodos especiais ---
    def __str__(self) -> str:
        return (
            f"{self.TIPO} {self.modelo} ({self.marca}) "
            f"- Placa: {self.placa} | KM: {self.quilometragem} | Status: {self.status}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(placa='{self.placa}', "
            f"marca='{self.marca}', modelo='{self.modelo}', ano={self.ano})"
        )

    def __eq__(self, other: object) -> bool:
        """Compara dois veículos pela placa."""
        if not isinstance(other, Veiculo):
            return False
        return self.placa == other.placa

    def __hash__(self) -> int:
        return hash(self.placa)

    def __lt__(self, other: "Veiculo") -> bool:
        """Ordena veículos pela quilometragem."""
        if not isinstance(other, Veiculo):
            return NotImplemented
        return self.quilometragem < other.quilometragem

    def __iter__(self):
        """Itera sobre o histórico de manutenções."""
        return iter(self.historico_manutencoes)


class Carro(Veiculo):
    """Carro (CNH B ou superior)."""

    TIPO = "Carro"


class Moto(Veiculo):
    """Moto (CNH A)."""

    TIPO = "Moto"


class Caminhao(Veiculo):
    """Caminhão (CNH C ou superior)."""

    TIPO = "Caminhao"


_CLASSES: dict[str, type[Veiculo]] = {
    "carro": Carro,
    "moto": Moto,
    "caminhao": Caminhao,
    "caminhão": Caminhao,
}


def classe_por_tipo(tipo: str) -> type[Veiculo]:
    """Retorna a subclasse de Veiculo correspondente ao nome do tipo."""
    try:
        return _CLASSES[tipo.strip().lower()]
    except KeyError:
        raise ValueError(
            f"Tipo de veículo inválido: '{tipo}'. Use: carro, moto ou caminhao."
        ) from None


def criar_veiculo(
    tipo: str, placa: str, marca: str, modelo: str, ano: int,
    quilometragem: float, consumo_medio: float, *, settings: Settings | None = None,
) -> Veiculo:
    """Factory de veículos pelo nome do tipo."""
    return classe_por_tipo(tipo)(
        placa, marca, modelo, ano, quilometragem, consumo_medio, settings=settings
    )