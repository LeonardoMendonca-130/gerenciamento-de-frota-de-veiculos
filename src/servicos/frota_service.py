# src/servicos/frota_service.py
"""Camada de serviço: orquestra domínio e persistência."""
from __future__ import annotations

from datetime import date
from typing import Any

from src.config import Settings, get_settings
from src.excecoes import AlocacaoInvalidaError, NaoEncontradoError, RepositorioError
from src.modelos.estrategias import obter_estrategia
from src.modelos.motorista import Motorista
from src.modelos.registros import Manutencao, Viagem
from src.modelos.veiculo import Veiculo, criar_veiculo
from src.repositorios.base import RepositorioBase
from src.servicos.relatorios import gerar_relatorio

CAMPOS_VEICULO = {"marca", "modelo", "ano", "quilometragem", "consumo_medio"}
CAMPOS_MOTORISTA = {"nome", "cnh_categoria", "tempo_experiencia_anos"}


def _hoje() -> str:
    return date.today().strftime("%d/%m/%Y")


class FrotaService:
    """Casos de uso do sistema; persiste o estado após cada operação."""

    def __init__(self, repositorio: RepositorioBase, settings: Settings | None = None) -> None:
        self._repo = repositorio
        self.settings = settings or get_settings()
        self._veiculos: dict[str, Veiculo] = {}
        self._motoristas: dict[str, Motorista] = {}
        self.carregar()

    # --- Persistência ---
    def carregar(self) -> None:
        """Reconstrói os objetos de domínio a partir do repositório."""
        dados = self._repo.ler_dados()
        try:
            lista_v = dados.get("veiculos", [])
            veiculos = [Veiculo.de_dict(d, self.settings) for d in lista_v]
            motoristas = [Motorista.de_dict(d) for d in dados.get("motoristas", [])]
        except (KeyError, TypeError, ValueError, AttributeError) as erro:
            raise RepositorioError(f"Dados persistidos inválidos: {erro!r}") from erro
        self._veiculos = {v.placa: v for v in veiculos}
        self._motoristas = {m.cpf: m for m in motoristas}
        for dados_v, veiculo in zip(lista_v, veiculos):
            cpf = dados_v.get("motorista_cpf")
            if cpf in self._motoristas:
                veiculo.motorista_alocado = self._motoristas[cpf]

    def salvar(self) -> None:
        """Grava o estado atual no repositório."""
        self._repo.salvar_dados({
            "veiculos": [v.para_dict() for v in self._veiculos.values()],
            "motoristas": [m.para_dict() for m in self._motoristas.values()],
        })

    # --- Consultas ---
    @property
    def veiculos(self) -> list[Veiculo]:
        return list(self._veiculos.values())

    @property
    def motoristas(self) -> list[Motorista]:
        return list(self._motoristas.values())

    def buscar_veiculo(self, placa: str) -> Veiculo:
        try:
            return self._veiculos[placa.strip().upper()]
        except KeyError:
            raise NaoEncontradoError(f"Veículo '{placa}' não encontrado.") from None

    def buscar_motorista(self, cpf: str) -> Motorista:
        try:
            return self._motoristas[cpf.strip()]
        except KeyError:
            raise NaoEncontradoError(f"Motorista com CPF '{cpf}' não encontrado.") from None

    # --- CRUD de veículos ---
    def cadastrar_veiculo(
        self, tipo: str, placa: str, marca: str, modelo: str,
        ano: int, quilometragem: float, consumo_medio: float,
    ) -> Veiculo:
        if placa.strip().upper() in self._veiculos:
            raise ValueError(f"Já existe um veículo com a placa {placa.strip().upper()}.")
        v = criar_veiculo(tipo, placa, marca, modelo, ano, quilometragem,
                          consumo_medio, settings=self.settings)
        v.registrar_evento("entrada", "Veículo cadastrado na frota.")
        self._veiculos[v.placa] = v
        self.salvar()
        return v

    def atualizar_veiculo(self, placa: str, **campos: Any) -> Veiculo:
        desconhecidos = set(campos) - CAMPOS_VEICULO
        if desconhecidos:
            raise ValueError(f"Campos não editáveis: {sorted(desconhecidos)}.")
        v = self.buscar_veiculo(placa)
        anteriores = {c: getattr(v, c) for c in campos}
        try:
            for campo, valor in campos.items():
                setattr(v, campo, valor)
        except ValueError:
            for campo, valor in anteriores.items():
                setattr(v, campo, valor)
            raise
        self.salvar()
        return v

    def remover_veiculo(self, placa: str) -> None:
        v = self.buscar_veiculo(placa)
        if v.motorista_alocado is not None:
            raise AlocacaoInvalidaError("Libere o motorista antes de remover o veículo.")
        del self._veiculos[v.placa]
        self.salvar()

    # --- CRUD de motoristas ---
    def cadastrar_motorista(self, nome: str, cpf: str, cnh_categoria: str,
                            tempo_experiencia_anos: int) -> Motorista:
        if cpf.strip() in self._motoristas:
            raise ValueError(f"Já existe um motorista com o CPF {cpf.strip()}.")
        m = Motorista(nome, cpf, cnh_categoria, tempo_experiencia_anos)
        self._motoristas[m.cpf] = m
        self.salvar()
        return m

    def editar_motorista(self, cpf: str, **campos: Any) -> Motorista:
        desconhecidos = set(campos) - CAMPOS_MOTORISTA
        if desconhecidos:
            raise ValueError(f"Campos não editáveis: {sorted(desconhecidos)}.")
        m = self.buscar_motorista(cpf)
        anteriores = {c: getattr(m, c) for c in campos}
        try:
            for campo, valor in campos.items():
                setattr(m, campo, valor)
        except ValueError:
            for campo, valor in anteriores.items():
                setattr(m, campo, valor)
            raise
        self.salvar()
        return m

    def remover_motorista(self, cpf: str) -> None:
        m = self.buscar_motorista(cpf)
        if not m.disponivel:
            raise AlocacaoInvalidaError("Motorista em viagem não pode ser removido.")
        del self._motoristas[m.cpf]
        self.salvar()

    # --- Alocação e viagens ---
    def alocar(self, placa: str, cpf: str) -> Veiculo:
        v = self.buscar_veiculo(placa)
        v.alocar_motorista(self.buscar_motorista(cpf))
        self.salvar()
        return v

    def liberar(self, placa: str) -> Veiculo:
        v = self.buscar_veiculo(placa)
        v.desalocar_motorista()
        self.salvar()
        return v

    def registrar_viagem(self, placa: str, origem: str, destino: str,
                         distancia: float) -> Viagem:
        viagem = self.buscar_veiculo(placa).registrar_viagem(origem, destino, distancia)
        self.salvar()
        return viagem

    # --- Abastecimento e manutenção ---
    def registrar_abastecimento(self, placa: str, litros: float, valor: float,
                                tipo_combustivel: str = "gasolina",
                                data: str | None = None) -> Veiculo:
        v = self.buscar_veiculo(placa)
        v.abastecer(data or _hoje(), tipo_combustivel, litros, valor)
        self.salvar()
        return v

    def estimar_custo_manutencao(self, estrategia: str, custo_pecas: float = 0.0) -> float:
        """Calcula o custo usando a Strategy e o custo base do settings.json."""
        est = obter_estrategia(estrategia)
        return est.calcular(self.settings.custo_base_manutencao(est.nome), custo_pecas)

    def enviar_para_manutencao(self, placa: str, tipo: str, descricao: str,
                               estrategia: str = "basica", custo_pecas: float = 0.0,
                               data: str | None = None) -> Manutencao:
        v = self.buscar_veiculo(placa)
        custo = self.estimar_custo_manutencao(estrategia, custo_pecas)
        manutencao = Manutencao(data or _hoje(), tipo, custo, descricao)
        v.enviar_para_manutencao(manutencao)
        self.salvar()
        return manutencao

    def concluir_manutencao(self, placa: str) -> Veiculo:
        v = self.buscar_veiculo(placa)
        v.concluir_manutencao()
        self.salvar()
        return v

    def desativar_veiculo(self, placa: str) -> Veiculo:
        v = self.buscar_veiculo(placa)
        v.alterar_status("INATIVO")
        self.salvar()
        return v

    # --- Relatórios e seed ---
    def gerar_relatorio(self, nome: str) -> str:
        return gerar_relatorio(nome, self.veiculos, self.motoristas)

    def popular_seed(self) -> bool:
        """Carrega dados de exemplo. Retorna False se já houver dados."""
        if self._veiculos or self._motoristas:
            return False
        self.cadastrar_veiculo("carro", "ABC1D23", "Toyota", "Corolla", 2022, 12000, 12.5)
        self.cadastrar_veiculo("carro", "XYZ9K88", "Fiat", "Argo", 2021, 30000, 13.0)
        self.cadastrar_veiculo("moto", "MOT0A11", "Honda", "CG 160", 2021, 5000, 40.0)
        self.cadastrar_veiculo("caminhao", "CAM1C22", "Volvo", "FH 540", 2019, 120000, 3.5)
        self.cadastrar_motorista("João Silva", "111.111.111-11", "B", 5)
        self.cadastrar_motorista("Maria Souza", "222.222.222-22", "D", 8)
        self.cadastrar_motorista("Carlos Lima", "333.333.333-33", "A", 3)

        self.alocar("ABC1D23", "111.111.111-11")
        self.registrar_viagem("ABC1D23", "Juazeiro do Norte", "Fortaleza", 520)
        self.registrar_abastecimento("ABC1D23", 40, 240.0, "gasolina")
        self.liberar("ABC1D23")

        self.alocar("XYZ9K88", "222.222.222-22")
        self.registrar_viagem("XYZ9K88", "Juazeiro do Norte", "Crato", 100)
        self.registrar_abastecimento("XYZ9K88", 20, 118.0, "gasolina")  # consumo baixo
        self.liberar("XYZ9K88")

        self.alocar("CAM1C22", "222.222.222-22")
        self.registrar_viagem("CAM1C22", "Juazeiro do Norte", "Recife", 560)
        self.registrar_abastecimento("CAM1C22", 140, 800.0, "diesel")
        self.liberar("CAM1C22")

        self.enviar_para_manutencao("MOT0A11", "preventiva", "Troca de óleo", "basica", 40.0)
        return True