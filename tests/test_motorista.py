import pytest
from src.modelos import Motorista, Viagem


def test_criacao_motorista_valido():
    """Testa a criação de um motorista com atributos válidos."""
    motorista = Motorista(
        nome="João Silva",
        cpf="123.456.789-00",
        cnh_categoria="b",
        tempo_experiencia_anos=5,
    )
    assert motorista.nome == "João Silva"
    assert motorista.cnh_categoria == "B"  # Deve converter para maiúsculo
    assert motorista.tempo_experiencia_anos == 5
    assert motorista.disponivel is True


def test_registrar_viagem():
    """Testa o registro de uma viagem no histórico do motorista."""
    motorista = Motorista("Maria Souza", "111.222.333-44", "D", 8)
    viagem = Viagem("Juazeiro do Norte", "Crato", 15.0)

    motorista.registrar_viagem(viagem)

    assert len(motorista.historico_viagens) == 1
    assert motorista.historico_viagens[0].origem == "Juazeiro do Norte"


def test_erro_cnh_invalida():
    """Garante que CNHs fora do padrão A-E disparem exceção."""
    with pytest.raises(ValueError):
        Motorista("Carlos", "000", "Z", 2)


def test_erro_experiencia_negativa():
    """Garante que anos de experiência negativos disparem exceção."""
    with pytest.raises(ValueError):
        Motorista("Ana", "000", "A", -1)