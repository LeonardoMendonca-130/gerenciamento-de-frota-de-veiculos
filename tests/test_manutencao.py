import pytest

from src.config import Settings
from src.excecoes import ManutencaoInvalidaError
from src.modelos import Basica, Carro, Complexa, Manutencao, Motorista, Pesada, obter_estrategia


@pytest.fixture
def carro():
    return Carro("ABC1D23", "Toyota", "Corolla", 2022, 10000.0, 12.0)


def test_inativo_nao_volta_a_ativo(carro):
    carro.alterar_status("INATIVO")
    with pytest.raises(ManutencaoInvalidaError):
        carro.alterar_status("ATIVO")


def test_concluir_sem_estar_em_manutencao_falha(carro):
    with pytest.raises(ManutencaoInvalidaError):
        carro.concluir_manutencao()


def test_enviar_duas_vezes_nao_duplica_historico(carro):
    carro.enviar_para_manutencao(Manutencao("01/11/2026", "corretiva", 100.0, "Pneu"))
    with pytest.raises(ManutencaoInvalidaError):
        carro.enviar_para_manutencao(Manutencao("02/11/2026", "corretiva", 100.0, "Óleo"))
    assert len(carro.historico_manutencoes) == 1


def test_registrar_manutencao_exige_tipo_correto(carro):
    with pytest.raises(TypeError):
        carro.registrar_manutencao("não sou uma manutenção")


def test_manutencao_invalida():
    with pytest.raises(ManutencaoInvalidaError):
        Manutencao("01/11/2026", "estética", 100.0, "x")
    with pytest.raises(ManutencaoInvalidaError):
        Manutencao("01/11/2026", "corretiva", -1.0, "x")


def test_nao_envia_para_manutencao_com_motorista_alocado(carro):
    carro.alocar_motorista(Motorista("João", "123", "B", 5))
    with pytest.raises(ManutencaoInvalidaError):
        carro.enviar_para_manutencao(Manutencao("01/11/2026", "corretiva", 100.0, "x"))
    assert carro.status == "ATIVO"


def test_estrategias_de_custo():
    assert Basica().calcular(150.0, 50.0) == 200.0
    assert Complexa().calcular(400.0, 100.0) == 520.0
    assert Pesada().calcular(900.0, 100.0) == 1500.0
    assert obter_estrategia("PESADA").nome == "pesada"
    with pytest.raises(ValueError):
        obter_estrategia("inexistente")


def test_politicas_vem_do_settings_e_sao_configuraveis():
    s = Settings({"limite_km_revisao_preventiva": 500})
    carro = Carro("ABC1D23", "Toyota", "Corolla", 2022, 1000.0, 12.0, settings=s)
    carro.quilometragem = 1500.0
    assert carro.revisao_preventiva_pendente is True
    assert Settings().cnhs_permitidas("Carro") == {"B", "C", "D", "E"}
    assert Settings().cnhs_permitidas("Moto") == {"A"}
    assert Settings().cnhs_permitidas("Caminhao") == {"C", "D", "E"}