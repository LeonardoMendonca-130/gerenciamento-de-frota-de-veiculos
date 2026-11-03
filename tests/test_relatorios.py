import pytest

from src.modelos import Caminhao, Carro, Moto, Veiculo


def test_consumo_real_calculado_por_km_e_litros():
    carro = Carro("ABC1D23", "Toyota", "Corolla", 2022, 1000.0, 12.0)
    carro.abastecer("01/11/2026", "gasolina", 40.0, 240.0)
    carro.quilometragem = 1400.0
    assert carro.consumo_real == pytest.approx(10.0)
    assert carro.litros_totais == 40.0
    assert carro.gasto_total_combustivel == 240.0


def test_consumo_real_indisponivel_sem_dados():
    carro = Carro("ABC1D23", "Toyota", "Corolla", 2022, 1000.0, 12.0)
    assert carro.consumo_real is None
    assert carro.consumo_efetivo == 12.0


def test_abastecimento_invalido():
    carro = Carro("ABC1D23", "Toyota", "Corolla", 2022, 1000.0, 12.0)
    with pytest.raises(ValueError):
        carro.abastecer("01/11/2026", "gasolina", 0, 100.0)


def test_consumo_fora_da_faixa_por_tipo():
    assert Carro("AAA1A11", "Fiat", "Uno", 2018, 0, 5.0).consumo_fora_da_faixa is True
    assert Carro("AAA1A12", "Fiat", "Uno", 2018, 0, 12.0).consumo_fora_da_faixa is False
    assert Moto("AAA1A13", "Honda", "CG", 2020, 0, 40.0).consumo_fora_da_faixa is False
    assert Caminhao("AAA1A14", "Volvo", "FH", 2019, 0, 4.0).consumo_fora_da_faixa is False


def test_veiculo_abstrato_nao_instancia():
    with pytest.raises(TypeError):
        Veiculo("ABC1D23", "X", "Y", 2020, 0, 10.0)