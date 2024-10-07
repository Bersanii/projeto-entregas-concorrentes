# Vitor Bersani Balan
# Juliano dos Reis Cruz

import os
import sys
import threading
import time
import random

# #######################
# Classes
# #######################

class Encomenda:
  def __init__(self, id):
    self.id = id

class Veiculo:
  def __init__(self, id, status = 'parado'):
    self.id = id
    self.status = status
    self.ponto = None

  def display_info(self):
    print(f'{self.id:<7} | {self.status:<15} | {self.ponto}')

class Ponto:
  def __init__(self, id):
    self.id = id

# #######################
# Globais
# #######################

t_0 = time.time()
mutex = threading.Lock()

threads_encomendas = []
encomendas = []
threads_veiculos = []
veiculos = []
threads_pontos = []
pontos = []

# #######################
# Monitor
# #######################

def thread_monitor():
  while True:
    # Limpar a tela (compatível com Windows e Unix)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"Hora atual: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    
    print(f'{'Veículo':<7} | {'Status':<15} | {'Ponto':<5}')
    print('------------------------------------------')
    for veiculo in veiculos:
      veiculo.display_info()

    print("\nPressione Ctrl+C para sair.")
    
    # Esperar por um segundo antes de atualizar novamente
    time.sleep(1)

# #######################
# Lógica
# #######################

def thread_veiculo(id):
  veiculo = Veiculo(id)
  veiculos.append(veiculo)

  while True:
    if veiculo.status == 'parado':
      veiculo.status = 'em_transito'
    else:
      veiculo.status = 'parado'
    time.sleep(random.uniform(0, 10))

if __name__ == '__main__':
  if len(sys.argv) < 5:
    print('Erro: Quantidade de argumentos inválida, garanta que está informando os valores de S C P A como argumentos')
    sys.exit()
  S, C, P, A = sys.argv[1:]
  # Fazer validação dos param de entrada
  print(S, C, P, A)

  # Criação dos veículos
  for i in range(0, int(C)):
    thread = threading.Thread(target=thread_veiculo,args=(i,))
    thread.daemon = True
    thread.start()
    threads_veiculos.append(thread)

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