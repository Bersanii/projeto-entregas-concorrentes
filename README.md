# Simulação de Rede de Entregas - Projeto de Sistemas Operacionais

Integrantes:
- Vitor Bersani Balan
- Juliano dos Reis Cruz
- André Augusto Costa Dionísio

## Descrição do Projeto

- Este projeto tem como objetivo a implementação de uma aplicação concorrente que simula uma rede de entregas, em que encomendas são transportadas por veículos de um ponto de
redistribuição até outro. 
- A sincronização é feita com uso de semáforos e variáveis de trava com o uso de threads para representar os veículos, encomendas e pontos de redistribuição. 
- O programa exibe monitoramento em tempo real e gera arquivos de rastro no disco para cada emcomenda entregue.

## Requisitos

- Python 3 (ou superior)
- Importações Python:
  - threading
  - time
  - random
  - os
  - sys

## Funcionalidades

- **Simulação de veículos**: Os veículos se movem entre pontos de redistribuição, transportando encomendas.
- **Gerenciamento de encomendas**: Cada encomenda possui um ponto de origem e destino, sendo transportada por veículos.
- **Monitoramento em tempo real**: O sistema exibe o status de todos os veículos, encomendas e pontos de redistribuição.
- **Arquivos de rastro**: Para cada encomenda, é gerado um arquivo com o histórico das entregas.

## Como Usar

### Argumentos de Entrada

O programa recebe os seguintes argumentos na linha de comando ao ser executado:

```bash
python simulacao.py S C P A
```

Onde:

- `S` é o número de pontos de redistribuição (S ≥ 1)
- `C` é o número de veículos (C ≥ 1)
- `P` é o número de encomendas (P ≥ 1)
- `A` é a quantidade de espaços de carga por veículo (A ≥ 1)

### Exemplo de Execução:
```bash
python simulacao.py 5 3 10 2
```

Este comando irá iniciar a simulação com:

- 5 pontos de redistribuição
- 3 veículos
- 10 encomendas
- Cada veículo terá 2 espaços de carga

## Estrutura do Código

### Classes Principais

#### 1. **Encomenda**

Representa uma encomenda a ser transportada entre os pontos de redistribuição.

- **Atributos**:
  - `id`: ID da encomenda.
  - `origem`: Ponto de origem da encomenda.
  - `destino`: Ponto de destino da encomenda.
  - `entregue`: Status da encomenda, indicando se foi entregue.
  - `tempo_descarga`: Tempo aleatório para a encomenda ser descarregada no ponto de destino.

- **Métodos**:
  - `display_info`: Exibe as informações da encomenda.

#### 2. **Veículo**

Representa um veículo responsável pelo transporte das encomendas.

- **Atributos**:
  - `id`: ID do veículo.
  - `espacos`: Quantidade de espaços de carga disponíveis no veículo.
  - `status`: Status atual do veículo (exemplo: "esperando", "em_transito").
  - `ponto`: Ponto de redistribuição atual do veículo.
  - `encomendas`: Lista de encomendas carregadas no veículo.
  - `tempo_viagem_atual`: Tempo aleatório para o veículo viajar de um ponto a outro.

- **Métodos**:
  - `display_info`: Exibe as informações do veículo.

#### 3. **Ponto**

Representa um ponto de redistribuição onde as encomendas são armazenadas antes de serem carregadas pelos veículos.

- **Atributos**:
  - `id`: ID do ponto.
  - `aguardando_despacho`: Lista de encomendas aguardando para serem carregadas no veículo.
  - `veiculos_aguardando`: Lista de veículos aguardando para carregar encomendas.
  - `ocupado`: Status que indica se o ponto está ocupado por um veículo ou não.

- **Métodos**:
  - `display_info`: Exibe as informações sobre o ponto de redistribuição.

### Threads

O programa utiliza múltiplas threads para simular a movimentação simultânea dos veículos, encomendas e pontos de redistribuição. As threads principais são:

- **thread_monitor**: Responsável por exibir as informações de monitoramento em tempo real na tela.
- **thread_veiculo**: Simula a movimentação de um veículo entre os pontos de redistribuição.
- **thread_encomenda**: Simula o transporte de uma encomenda entre os pontos de origem e destino.
- **thread_ponto**: Gerencia os pontos de redistribuição, controlando o despacho de encomendas e a espera dos veículos.

### Fluxo de Execução

1. O programa cria as threads para as encomendas, veículos e pontos de redistribuição.
2. As encomendas são criadas com origem e destino aleatórios.
3. Os veículos começam a circular entre os pontos de redistribuição, carregando e descarregando as encomendas.
4. As encomendas são entregues ao longo do tempo, e o status de cada uma é atualizado.
5. O monitoramento em tempo real exibe a situação atual do sistema a cada segundo.
6. Quando todas as encomendas forem entregues, os veículos param e o programa finaliza.

## Saídas do Programa

- **Tela de Monitoramento**: Exibe informações sobre os veículos, encomendas e pontos de redistribuição.
- **Arquivos de Rastro**: Para cada encomenda, é gerado um arquivo de rastro contendo o histórico de sua movimentação, incluindo os horários de chegada ao ponto de origem, carga no veículo e descarga no ponto de destino.
