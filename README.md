# gerenciamento-de-frota-de-veiculos

## Definição do projeto e Funcionalidades
>Este projeto consiste em um sistema de gerenciamento de frota de veículos desenvolvido em Python como parte da disciplina de Programação Orientada a Objetos.
 
>O projeto objetiva gerenciar a frota de veículos e motoristas de uma empresa de transportes, permitindo o controle de manutenções, o histórico de abastecimentos, a alocação de viagens e a geração de relatórios operacionais e de custos.

## 🧩 Diagrama UML

```mermaid
classDiagram
    direction TB

    class Pessoa {
        -str _nome
        -str _cpf
        +nome str
        +cpf str
    }

    class Motorista {
        -str _cnh_categoria
        -int _tempo_experiencia_anos
        -bool _disponivel
        -list~Viagem~ _historico_viagens
        +CATEGORIAS_VALIDAS frozenset
        +total_viagens int
        +km_total float
        +registrar_viagem(viagem) None
        +para_dict() dict
        +de_dict(d)$ Motorista
    }

    class AbastecivelMixin {
        -list~Abastecimento~ _historico_abastecimentos
        +litros_totais float
        +gasto_total_combustivel float
        +abastecer(data, tipo_combustivel, litros, valor) None
    }

    class ManutenivelMixin {
        -StatusVeiculo _status
        -list~Manutencao~ _historico_manutencoes
        +status str
        +registrar_manutencao(manutencao) None
        +alterar_status(novo_status) None
        +enviar_para_manutencao(manutencao) None
        +concluir_manutencao() None
    }

    class Veiculo {
        <<abstract>>
        -str _placa
        -str _marca
        -str _modelo
        -int _ano
        -float _quilometragem
        -float _consumo_medio
        +TIPO str
        +motorista_alocado Motorista
        +cnhs_permitidas frozenset
        +revisao_preventiva_pendente bool
        +consumo_real float
        +consumo_efetivo float
        +consumo_fora_da_faixa bool
        +alocar_motorista(motorista) None
        +desalocar_motorista() None
        +registrar_viagem(origem, destino, distancia) Viagem
        +registrar_evento(tipo, descricao) None
        +para_dict() dict
        +de_dict(d)$ Veiculo
        +__str__() str
        +__repr__() str
        +__eq__(other) bool
        +__lt__(other) bool
        +__iter__() Iterator
    }

    class Carro { +TIPO = "Carro" }
    class Moto { +TIPO = "Moto" }
    class Caminhao { +TIPO = "Caminhao" }

    class Manutencao {
        +str data
        +str tipo
        +float custo
        +str descricao
    }
    class Abastecimento {
        +str data
        +str tipo_combustivel
        +float litros
        +float valor
    }
    class Viagem {
        +str origem
        +str destino
        +float distancia_percorrida
        +str placa
    }
    class Evento {
        +str data
        +str tipo
        +str descricao
    }

    class StatusVeiculo {
        <<enumeration>>
        ATIVO
        MANUTENCAO
        INATIVO
        +pode_ir_para(novo) bool
    }

    Pessoa <|-- Motorista
    AbastecivelMixin <|-- Veiculo
    ManutenivelMixin <|-- Veiculo
    Veiculo <|-- Carro
    Veiculo <|-- Moto
    Veiculo <|-- Caminhao

    Veiculo "1" *-- "*" Manutencao : historico
    Veiculo "1" *-- "*" Abastecimento : historico
    Veiculo "1" *-- "*" Evento : historico
    Motorista "1" *-- "*" Viagem : realiza
    Veiculo "0..1" --> "0..1" Motorista : alocado a
    ManutenivelMixin ..> StatusVeiculo : usa
```

## Arquitetura do Projeto

>Estrutura de Diretórios

```text
gerenciamento-de-frota-de-veiculos/
│
cli.py
src/
├── config.py, excecoes.py, settings.json
├── modelos/        pessoa, motorista, mixins, veiculo, registros, status, estrategias
├── repositorios/   base (interface), json_repository, sqlite_repository
└── servicos/       frota_service (casos de uso), relatorios
tests/
```

## Decisões de design
- **Herança múltipla:** `Veiculo(AbastecivelMixin, ManutenivelMixin)`. Cada mixin chama `super().__init__`, então o MRO inicializa tudo.
- **Encapsulamento:** atributos privados com `@property` e validações nos setters (km ≥ 0, consumo > 0, CNH válida...).
- **Métodos especiais:** `__str__`, `__repr__`, `__eq__` (placa), `__hash__`, `__lt__` (km) e `__iter__` (manutenções).
- **State/Enum:** `StatusVeiculo` com transições ATIVO↔MANUTENCAO e ATIVO→INATIVO. Veículo com motorista alocado não muda de status.
- **Strategy:** `Basica`, `Complexa` e `Pesada` calculam o custo de manutenção a partir de `custos_manutencao` no `settings.json`.
- **Repository:** `RepositorioBase` define o contrato. O domínio não conhece JSON nem SQLite; ele só expõe `para_dict`/`de_dict`.
- **Regras configuráveis (`settings.json`):** limite de km da revisão, faixa de consumo (global e por tipo), custos de manutenção e CNH mínima por tipo.
- **Revisão preventiva:** o contador de km parte do cadastro. Manutenção `preventiva` zera o contador. Com revisão pendente, a alocação é bloqueada (`PoliticaNaoAtendidaError`).
- **Consumo real:** (km rodados desde o cadastro) ÷ (litros abastecidos). Sem dados, usa o consumo declarado.
- **Exceções:** `ManutencaoInvalidaError`, `AlocacaoInvalidaError`, `PoliticaNaoAtendidaError`, `RepositorioError`, `NaoEncontradoError`.

## Como Executar o Sistema 
Atualmente o sistema encontra-se em fase de modelagem inicial.  
Para verificar a estrutura de módulos:
1. Clone o repositório.
2. Certifique-se de ter o Python 3.10+ instalado.
