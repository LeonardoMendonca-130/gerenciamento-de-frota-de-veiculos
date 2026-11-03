import pytest

from src.excecoes import AlocacaoInvalidaError, PoliticaNaoAtendidaError
from src.modelos import Caminhao, Carro, Manutencao, Moto, Motorista


@pytest.fixture
def carro():
    return Carro("ABC1D23", "Toyota", "Corolla", 2022, 10000.0, 12.0)


@pytest.fixture
def motorista_b():
    return Motorista("João Silva", "123.456.789-00", "B", 5)


def test_alocar_motorista_compativel(carro, motorista_b):
    carro.alocar_motorista(motorista_b)
    assert carro.motorista_alocado is motorista_b
    assert motorista_b.disponivel is False


def test_alocacao_bloqueada_em_manutencao(carro, motorista_b):
    carro.enviar_para_manutencao(Manutencao("01/11/2026", "corretiva", 300.0, "Freios"))
    with pytest.raises(AlocacaoInvalidaError):
        carro.alocar_motorista(motorista_b)


def test_alocacao_bloqueada_veiculo_inativo(carro, motorista_b):
    carro.alterar_status("INATIVO")
    with pytest.raises(AlocacaoInvalidaError):
        carro.alocar_motorista(motorista_b)


def test_cnh_b_nao_dirige_moto_nem_caminhao(motorista_b):
    moto = Moto("MOTO123", "Honda", "CG 160", 2021, 5000.0, 40.0)
    caminhao = Caminhao("CAM1C22", "Volvo", "FH", 2019, 90000.0, 3.5)
    with pytest.raises(PoliticaNaoAtendidaError):
        moto.alocar_motorista(motorista_b)
    with pytest.raises(PoliticaNaoAtendidaError):
        caminhao.alocar_motorista(motorista_b)


def test_cnh_superior_dirige_carro_e_caminhao(carro):
    motorista_d = Motorista("Maria", "111", "D", 8)
    carro.alocar_motorista(motorista_d)
    assert carro.motorista_alocado is motorista_d
    carro.desalocar_motorista()
    caminhao = Caminhao("CAM1C22", "Volvo", "FH", 2019, 90000.0, 3.5)
    caminhao.alocar_motorista(motorista_d)
    assert caminhao.motorista_alocado is motorista_d


def test_motorista_indisponivel_nao_pode_ser_alocado(carro, motorista_b):
    carro.alocar_motorista(motorista_b)
    outro = Carro("XYZ9999", "Fiat", "Uno", 2018, 50000.0, 14.0)
    with pytest.raises(AlocacaoInvalidaError):
        outro.alocar_motorista(motorista_b)


def test_viagem_atualiza_quilometragem_e_historico(carro, motorista_b):
    carro.alocar_motorista(motorista_b)
    carro.registrar_viagem("Juazeiro do Norte", "Crato", 15.0)
    assert carro.quilometragem == 10015.0
    assert motorista_b.total_viagens == 1
    assert motorista_b.historico_viagens[0].placa == "ABC1D23"


def test_viagem_sem_motorista_falha(carro):
    with pytest.raises(AlocacaoInvalidaError):
        carro.registrar_viagem("A", "B", 10.0)


def test_desalocar_libera_motorista(carro, motorista_b):
    carro.alocar_motorista(motorista_b)
    carro.desalocar_motorista()
    assert carro.motorista_alocado is None
    assert motorista_b.disponivel is True


def test_revisao_preventiva_bloqueia_alocacao_ate_ser_feita(carro, motorista_b):
    carro.alocar_motorista(motorista_b)
    carro.registrar_viagem("Juazeiro do Norte", "Brasília", 10000.0)
    carro.desalocar_motorista()
    assert carro.revisao_preventiva_pendente is True
    with pytest.raises(PoliticaNaoAtendidaError):
        carro.alocar_motorista(motorista_b)

    carro.enviar_para_manutencao(Manutencao("01/11/2026", "preventiva", 150.0, "Revisão"))
    carro.concluir_manutencao()
    assert carro.revisao_preventiva_pendente is False
    carro.alocar_motorista(motorista_b)