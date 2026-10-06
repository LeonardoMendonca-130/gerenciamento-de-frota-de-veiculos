import pytest
from src.modelos import Carro, Moto, Caminhao, Manutencao


def test_encapsulamento_quilometragem():
    """Testa leitura e validação via setter de quilometragem."""
    carro = Carro("ABC1D23", "Toyota", "Corolla", 2022, 10000.0, 12.0)
    assert carro.quilometragem == 10000.0

    # Atualização válida
    carro.quilometragem = 12000.0
    assert carro.quilometragem == 12000.0

    # Atribuição inválida
    with pytest.raises(ValueError):
        carro.quilometragem = -100.0


def test_alterar_status_e_manutenivel_mixin():
    """Testa transição de status vinda do ManutenivelMixin."""
    carro = Carro("ABC1D23", "Toyota", "Corolla", 2022, 10000.0, 12.0)
    assert carro.status == "ATIVO"

    carro.alterar_status("MANUTENCAO")
    assert carro.status == "MANUTENCAO"

    with pytest.raises(ValueError):
        carro.alterar_status("INVALIDO")


def test_metodos_especiais_eq_e_lt():
    """Testa comparação por placa (__eq__) e ordenação por KM (__lt__)."""
    carro1 = Carro("ABC1234", "Ford", "Ka", 2020, 15000.0, 13.0)
    carro2 = Carro("abc1234", "Ford", "Ka", 2020, 25000.0, 13.0)
    carro3 = Carro("XYZ9999", "Fiat", "Uno", 2018, 50000.0, 14.0)

    # Igualdade por placa
    assert carro1 == carro2
    assert carro1 != carro3

    # Comparação < por quilometragem
    assert carro1 < carro3
    lista_ordenada = sorted([carro3, carro1])
    assert lista_ordenada[0] == carro1


def test_iterador_historico_manutencoes():
    """Testa o método __iter__ sobre o histórico de manutenções."""
    moto = Moto("MOTO123", "Honda", "CG 160", 2021, 5000.0, 40.0)
    manut = Manutencao("01/10/2026", "preventiva", 150.0, "Troca de óleo")

    moto.registrar_manutencao(manut)

    manutencoes_lista = list(moto)  # Utiliza __iter__
    assert len(manutencoes_lista) == 1
    assert manutencoes_lista[0].custo == 150.0