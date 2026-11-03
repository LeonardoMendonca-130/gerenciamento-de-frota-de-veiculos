"""Relatórios operacionais e de custos da frota."""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from src.modelos.motorista import Motorista
from src.modelos.veiculo import Veiculo

NOMES_RELATORIOS = ("status", "custos", "eficiencia", "viagens", "km", "consumo")


def _moeda(valor: float) -> str:
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def _titulo(texto: str) -> str:
    return f"{'=' * 50}\n{texto}\n{'=' * 50}"


# --- Dados (funções puras, fáceis de testar) ---
def custos_manutencao_por_tipo(veiculos: Iterable[Veiculo]) -> dict[str, dict[str, Any]]:
    """Quantidade, custo total e custo médio de manutenção por tipo de veículo."""
    agrupado: dict[str, list[float]] = defaultdict(list)
    for v in veiculos:
        agrupado[v.TIPO].extend(m.custo for m in v.historico_manutencoes)
    return {
        tipo: {
            "quantidade": len(custos),
            "total": sum(custos),
            "media": sum(custos) / len(custos) if custos else 0.0,
        }
        for tipo, custos in sorted(agrupado.items())
    }


def ranking_eficiencia(veiculos: Iterable[Veiculo]) -> list[tuple[Veiculo, float, str]]:
    """Veículos ordenados do mais para o menos eficiente (km/l)."""
    itens = [
        (v, v.consumo_efetivo, "medido" if v.consumo_real is not None else "declarado")
        for v in veiculos
    ]
    return sorted(itens, key=lambda i: i[1], reverse=True)


def viagens_por_motorista(motoristas: Iterable[Motorista]) -> list[tuple[str, int, float]]:
    """(nome, total de viagens, km total) por motorista, do maior para o menor."""
    itens = [(m.nome, m.total_viagens, m.km_total) for m in motoristas]
    return sorted(itens, key=lambda i: (i[1], i[2]), reverse=True)


def km_media_por_tipo(veiculos: Iterable[Veiculo]) -> dict[str, float]:
    """Quilometragem média por tipo de veículo."""
    agrupado: dict[str, list[float]] = defaultdict(list)
    for v in veiculos:
        agrupado[v.TIPO].append(v.quilometragem)
    return {t: sum(k) / len(k) for t, k in sorted(agrupado.items())}


# --- Relatórios formatados ---
def relatorio_status(veiculos: Iterable[Veiculo]) -> str:
    """Veículos agrupados por status (ATIVO, MANUTENCAO, INATIVO)."""
    veiculos = list(veiculos)
    linhas = [_titulo("RELATÓRIO DE VEÍCULOS POR STATUS")]
    if not veiculos:
        linhas.append("Nenhum veículo registrado.")
    for status, rotulo in (("ATIVO", "ATIVOS"), ("MANUTENCAO", "EM MANUTENÇÃO"),
                           ("INATIVO", "INATIVOS")):
        grupo = [v for v in veiculos if v.status == status]
        linhas.append(f"\n[ {rotulo} ]: {len(grupo)}")
        linhas.extend(f"  - {v.placa} ({v.modelo})" for v in grupo)
    return "\n".join(linhas)


def relatorio_custos_manutencao(veiculos: Iterable[Veiculo]) -> str:
    """Custo total e médio de manutenção por tipo de veículo."""
    linhas = [_titulo("CUSTOS DE MANUTENÇÃO POR TIPO")]
    dados = custos_manutencao_por_tipo(veiculos)
    if not dados:
        linhas.append("Nenhum veículo registrado.")
    for tipo, d in dados.items():
        linhas.append(
            f"{tipo:<9} | serviços: {d['quantidade']:>3} | "
            f"total: {_moeda(d['total'])} | média: {_moeda(d['media'])}"
        )
    return "\n".join(linhas)


def relatorio_eficiencia(veiculos: Iterable[Veiculo]) -> str:
    """Ranking de veículos por eficiência de combustível."""
    linhas = [_titulo("RANKING DE EFICIÊNCIA DE COMBUSTÍVEL")]
    ranking = ranking_eficiencia(veiculos)
    if not ranking:
        linhas.append("Nenhum veículo registrado.")
    for pos, (v, consumo, origem) in enumerate(ranking, start=1):
        linhas.append(f"{pos:>2}. {v.placa} ({v.TIPO} {v.modelo}): {consumo:.2f} km/l [{origem}]")
    return "\n".join(linhas)


def relatorio_viagens_motorista(motoristas: Iterable[Motorista]) -> str:
    """Total de viagens por motorista."""
    linhas = [_titulo("VIAGENS POR MOTORISTA")]
    dados = viagens_por_motorista(motoristas)
    if not dados:
        linhas.append("Nenhum motorista registrado.")
    for nome, total, km in dados:
        linhas.append(f"{nome:<25} | viagens: {total:>3} | km: {km:.1f}")
    return "\n".join(linhas)


def relatorio_km_medio(veiculos: Iterable[Veiculo]) -> str:
    """Quilometragem média por tipo de veículo."""
    linhas = [_titulo("QUILOMETRAGEM MÉDIA POR TIPO")]
    dados = km_media_por_tipo(veiculos)
    if not dados:
        linhas.append("Nenhum veículo registrado.")
    for tipo, media in dados.items():
        linhas.append(f"{tipo:<9} | {media:.1f} km")
    return "\n".join(linhas)


def relatorio_consumo(veiculos: Iterable[Veiculo]) -> str:
    """Alertas de desempenho: consumo fora da faixa e revisão preventiva pendente."""
    veiculos = list(veiculos)
    linhas = [_titulo("ALERTAS DE DESEMPENHO")]
    fora = [v for v in veiculos if v.consumo_fora_da_faixa]
    linhas.append(f"\n[ CONSUMO FORA DA FAIXA ]: {len(fora)}")
    for v in fora:
        minimo, maximo = v.faixa_consumo
        linhas.append(
            f"  ! {v.placa} ({v.TIPO}): {v.consumo_efetivo:.2f} km/l "
            f"(aceitável: {minimo:g} a {maximo:g})"
        )
    pendentes = [v for v in veiculos if v.revisao_preventiva_pendente]
    linhas.append(f"\n[ REVISÃO PREVENTIVA PENDENTE ]: {len(pendentes)}")
    for v in pendentes:
        linhas.append(f"  ! {v.placa} ({v.TIPO}): {v.km_desde_revisao:.0f} km desde a última revisão")
    return "\n".join(linhas)


def gerar_relatorio(
    nome: str, veiculos: Iterable[Veiculo], motoristas: Iterable[Motorista]
) -> str:
    """Gera um relatório pelo nome (ou 'todos')."""
    veiculos, motoristas = list(veiculos), list(motoristas)
    geradores = {
        "status": lambda: relatorio_status(veiculos),
        "custos": lambda: relatorio_custos_manutencao(veiculos),
        "eficiencia": lambda: relatorio_eficiencia(veiculos),
        "viagens": lambda: relatorio_viagens_motorista(motoristas),
        "km": lambda: relatorio_km_medio(veiculos),
        "consumo": lambda: relatorio_consumo(veiculos),
    }
    if nome == "todos":
        return "\n\n".join(g() for g in geradores.values())
    if nome not in geradores:
        raise ValueError(
            f"Relatório desconhecido: '{nome}'. Opções: {', '.join(NOMES_RELATORIOS)}, todos."
        )
    return geradores[nome]()