import pytest

from src.excecoes import (AlocacaoInvalidaError, NaoEncontradoError,
                          RepositorioError)
from src.repositorios.json_repository import JsonRepository
from src.repositorios.sqlite_repository import SqliteRepository
from src.servicos.frota_service import FrotaService


@pytest.fixture(params=["json", "sqlite"])
def repo(request, tmp_path):
    if request.param == "json":
        return JsonRepository(str(tmp_path / "dados.json"))
    return SqliteRepository(str(tmp_path / "dados.db"))


def test_repositorio_round_trip(repo):
    repo.salvar_dados({"veiculos": [{"placa": "A"}], "motoristas": []})
    assert repo.ler_dados()["veiculos"][0]["placa"] == "A"


def test_servico_persiste_e_recarrega_estado(repo):
    svc = FrotaService(repo)
    svc.cadastrar_veiculo("carro", "ABC1D23", "Toyota", "Corolla", 2022, 1000, 12.0)
    svc.cadastrar_motorista("João", "123", "B", 5)
    svc.alocar("abc1d23", "123")
    svc.registrar_viagem("ABC1D23", "A", "B", 50)
    svc.registrar_abastecimento("ABC1D23", 10, 60.0)

    novo = FrotaService(repo)  # mesmo repositório, novo serviço
    v = novo.buscar_veiculo("ABC1D23")
    assert v.quilometragem == 1050.0
    assert v.motorista_alocado is novo.buscar_motorista("123")
    assert novo.buscar_motorista("123").disponivel is False
    assert len(v.historico_abastecimentos) == 1
    assert v.consumo_real == pytest.approx(5.0)


def test_servico_regras_de_crud(repo):
    svc = FrotaService(repo)
    svc.cadastrar_veiculo("moto", "MOT0A11", "Honda", "CG", 2021, 0, 40)
    with pytest.raises(ValueError):
        svc.cadastrar_veiculo("moto", "mot0a11", "Honda", "CG", 2021, 0, 40)
    with pytest.raises(ValueError):
        svc.atualizar_veiculo("MOT0A11", quilometragem=-5)
    assert svc.buscar_veiculo("MOT0A11").quilometragem == 0.0
    svc.atualizar_veiculo("MOT0A11", modelo="CG 160")
    svc.remover_veiculo("MOT0A11")
    with pytest.raises(NaoEncontradoError):
        svc.buscar_veiculo("MOT0A11")


def test_nao_remove_veiculo_alocado(repo):
    svc = FrotaService(repo)
    svc.cadastrar_veiculo("carro", "ABC1D23", "Toyota", "Corolla", 2022, 0, 12)
    svc.cadastrar_motorista("João", "123", "B", 5)
    svc.alocar("ABC1D23", "123")
    with pytest.raises(AlocacaoInvalidaError):
        svc.remover_veiculo("ABC1D23")
    with pytest.raises(AlocacaoInvalidaError):
        svc.remover_motorista("123")


def test_seed_popula_apenas_uma_vez(repo):
    svc = FrotaService(repo)
    assert svc.popular_seed() is True
    assert svc.popular_seed() is False
    assert len(svc.veiculos) == 4


def test_json_corrompido_gera_repositorio_error(tmp_path):
    caminho = tmp_path / "ruim.json"
    caminho.write_text("{ isto não é json", encoding="utf-8")
    with pytest.raises(RepositorioError):
        FrotaService(JsonRepository(str(caminho)))