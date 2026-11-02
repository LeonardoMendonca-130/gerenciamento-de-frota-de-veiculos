"""Exceções customizadas do sistema de gerenciamento de frota."""


class FrotaError(Exception):
    """Classe base de todas as exceções do domínio."""


class ManutencaoInvalidaError(FrotaError, ValueError):
    """Manutenção ou transição de estado de manutenção inválida."""


class AlocacaoInvalidaError(FrotaError, ValueError):
    """Alocação de veículo/motorista inválida."""


class PoliticaNaoAtendidaError(FrotaError, ValueError):
    """Uma política configurável (CNH, revisão preventiva...) não foi atendida."""


class RepositorioError(FrotaError):
    """Falha ao ler ou gravar dados na camada de persistência."""


class NaoEncontradoError(FrotaError, LookupError):
    """Entidade (veículo ou motorista) não encontrada."""