# Vitor Bersani Balan
# Juliano dos Reis Cruz

import os
import sys
import threading
import time
import random
from typing import List

# #######################
# Classes
# #######################

class Encomenda:
  def __init__(self, id, origem, destino):
    self.id = id
    self.origem = origem
    self.destino = destino
    self.entregue = False
    self.tempo_descarga = random.randint(0, 10)

  def display_info(self):
    print(f'{self.id:<10} | {(str(self.origem)+'/'+str(self.destino)):<5} | {('Sim' if self.entregue else 'Não'):<8}')

# Status: esperando | descarregando | em_transito
class Veiculo:
  def __init__(self, id, espacos, ponto, status = 'esperando'):
    self.id = id
    self.espacos = espacos
    self.status = status
    self.ponto = ponto
    self.encomendas = []

  def display_info(self):
    print(f'{self.id:<7} | {self.status:<15} | {self.ponto:<5} | {(str(len(self.encomendas))+'/'+self.espacos):<7}')

class Ponto:
  def __init__(self, id, aguardando_despacho: List[int]):
    self.id = id
    self.aguardando_despacho = aguardando_despacho

  def display_info(self):
    print(f'{self.id:<5} | {', '.join(str(num) for num in self.aguardando_despacho):<15}')

# #######################
# Globais
# #######################

t_0 = time.time()
mutex = threading.Lock()

threads_encomendas = []
encomendas: List[Encomenda] = []
threads_veiculos = []
veiculos: List[Veiculo]  = []
threads_pontos = []
pontos: List[Ponto] = []

# #######################
# Monitor
# #######################

def thread_monitor():
  while True:
    # Limpar a tela (compatível com Windows e Unix)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"Hora atual: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    
    print(f'{'Veículo':<7} | {'Status':<15} | {'Ponto':<5} | {'Carga':<7}')
    print('---------------------------------------------------------------------')
    for veiculo in veiculos:
      veiculo.display_info()

    print()

    print(f'{'Encomenda':<10} | {'O/D':<5} | {'Entregue':<8}')
    print('---------------------------------------------------------------------')
    for encomenda in encomendas:
      encomenda.display_info()

    print()

    print(f'{'Ponto':<5} | {'Aguardando Desp.':<15}')
    print('---------------------------------------------------------------------')
    for ponto in pontos:
      ponto.display_info()

    print("\nPressione Ctrl+C para sair.")
    
    # Esperar por um segundo antes de atualizar novamente
    time.sleep(1)

# #######################
# Lógica
# #######################

def thread_veiculo(id, espacos, ponto):
  veiculo = Veiculo(id, espacos, ponto)
  veiculos.append(veiculo)

  while True:
    time.sleep(random.uniform(0, 10))

def thread_encomenda(id, origem, destino):
  encomenda = Encomenda(id, origem, destino)
  encomendas.append(encomenda)

  if encomenda.origem == encomenda.destino:
    encomenda.entregue = True
  
  while not encomenda.entregue:
    time.sleep(1)

def thread_ponto(id, aguardando_despacho):
  ponto = Ponto(id, aguardando_despacho)
  pontos.append(ponto)
  
  while len(ponto.aguardando_despacho) > 0:
    time.sleep(1)

if __name__ == '__main__':
  if len(sys.argv) < 5:
    print('Erro: Quantidade de argumentos inválida, garanta que está informando os valores de S C P A como argumentos')
    sys.exit()
  S, C, P, A = sys.argv[1:]
  # Fazer validação dos param de entrada
  print(S, C, P, A)

  # Criação das encomendas
  for i in range(0, int(P)):
    origem = random.randint(0, int(S))
    destino = random.randint(0, int(S))
    thread = threading.Thread(target=thread_encomenda,args=(i,origem,destino))
    thread.daemon = True
    thread.start()
    threads_encomendas.append(thread)

  # Criação dos veículos
  for i in range(0, int(C)):
    ponto_inicial = random.randint(0, int(S))
    thread = threading.Thread(target=thread_veiculo,args=(i, A, ponto_inicial))
    thread.daemon = True
    thread.start()
    threads_veiculos.append(thread)

  # Criação dos pontos
  for i in range(0, int(S)):
    aguardando_despacho = [ encomenda.id for encomenda in encomendas if encomenda.origem == i]
    thread = threading.Thread(target=thread_ponto,args=(i, aguardando_despacho))
    thread.daemon = True
    thread.start()
    threads_pontos.append(thread)

  monitor = threading.Thread(target=thread_monitor)
  monitor.daemon = True
  monitor.start()

  # Loop Principal que valida interrupções do usuário
  # OBS: pelas threads estarem em modo daemon elas só existem enquanto o main existir, por isso esse loop é necessário
  try:
    while True:
      time.sleep(10)
  except KeyboardInterrupt:
      print("\nEncerrando programa principal.")