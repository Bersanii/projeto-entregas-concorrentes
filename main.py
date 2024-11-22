# Vitor Bersani Balan
# Juliano dos Reis Cruz
# André Augusto Costa Dionísio

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
    self.horarios = {"chegada_origem": None, "carregamento": None, "descarregamento": None}
    self.id_veiculo = None

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
    self.tempo_viagem_atual = 0

  def display_info(self):
    print(f'{self.id:<7} | {self.status:<15} | {self.ponto:<5} | {(str(len(self.encomendas))+'/'+str(self.espacos)):<7}')


class Ponto:
  def __init__(self, id, aguardando_despacho: List[int]):
    self.id = id
    self.aguardando_despacho = aguardando_despacho
    self.veiculos_aguardando = [] # nao sendo usado, precisa ser implementado
    self.ocupado = threading.Semaphore(1)
    self.lock_fila = threading.Lock()

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

entregas_restantes = 0

programa_ativo = True

# #######################
# Monitor
# #######################

def thread_monitor():
  while programa_ativo:
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

  while entregas_restantes > 0 and programa_ativo:

    ponto_atual = pontos[veiculo.ponto - 1]

    # tentativa de entrar no ponto em que o veiculo se encontra
    ponto_atual.ocupado.acquire()
    

    with ponto_atual.lock_fila:
      
      for encomenda in veiculo.encomendas:

        # verifico se o destino da encomenda eh igual ao ponto em que o veiculo esta
        # tambem verifico se a encomenda ja nao consta como entregue
        if(encomenda.destino == ponto_atual.id) and (encomenda.entregue != True):
          veiculo.status = "descarregando"
          time.sleep(float(encomenda.tempo_descarga))
          encomenda.horarios["descarregamento"] = time.time()
          encomendas[encomenda.id].entregue = True
          encomenda.id_veiculo = veiculo.id
          veiculo.encomendas.remove(encomenda)
       
       # Essa parte nao quebrou o codigo
       #-------------------------------------------------------------------------------------

      # verifico se existem encomendas nesse ponto que precisam ser despachadas para outro e se tem espaco no veiculo
      
      
      if len(ponto_atual.aguardando_despacho) > 0:

        if(len(veiculo.encomendas) < veiculo.espacos):
          
          veiculo.status = "carregando"
          encomenda = encomendas[ponto_atual.aguardando_despacho.pop()]
          time.sleep(float(encomenda.tempo_descarga))
          encomenda.horarios["carregamento"] = time.time()
          veiculo.encomendas.append(encomenda)
          
          
      # Essa parte nao quebrou o codigo
      # -------------------------------------------------------------------------------------  



          


    ponto_atual.ocupado.release()      

    # Apos o veiculo fazer o que precisava ser feito no ponto, ele se movimenta em direcao ao proximo
    veiculo.status = "em_transito"
    veiculo.ponto = (veiculo.ponto + 1) % len(pontos)

    time.sleep(random.uniform(0, 10))

def thread_encomenda(id, origem, destino):
  
  global entregas_restantes

  encomenda = Encomenda(id, origem, destino)
  encomendas.append(encomenda)
  encomenda.horarios["chegada_origem"] = time.time()

  if encomenda.origem == encomenda.destino:
    encomenda.entregue = True
  
  while not encomenda.entregue:
    time.sleep(1)


  # No nomento em que o status entregue da encomenda fica true, ele entra no mutex e decresce o contador entregas_restantes 
  with mutex:
    entregas_restantes -=1

  with open(f"rastro_encomenda_{id}.txt", "w") as f:
    f.write(f"Encomenda {id}\n")
    f.write(f"Origem: {origem}, Destino: {destino}\n")
    f.write(f"Chegada na origem: {encomenda.horarios['chegada_origem']}\n")
    f.write(f"Carregada no veiculo {encomenda.id_veiculo} as {encomenda.horarios['carregamento']}\n")
    f.write(f"Descarregada as {encomenda.horarios['descarregamento']}\n")

def thread_ponto(id, aguardando_despacho):
  ponto = Ponto(id, aguardando_despacho)
  pontos.append(ponto)
  
  # Nessa parte aqui, temos que enquanto houver encomendas a serem despachadas, a thread nao eh finalizada
  # Precisariamos incluir nesse loop a condicao de existir encomendas com destino a esse ponto, ou seja, o ponto nao pode deixar de existir
  # se existir encomendas que precisam ser entregues aqui e ainda nao foram
  while programa_ativo:

    # verificar se ha encomendas destinadas ao ponto que ainda nao chegaram
    encomendas_pra_chegar_ponto = any(not encomenda.entregue and encomenda.destino == id for encomenda in encomendas)

    if not encomendas_pra_chegar_ponto and len(ponto.aguardando_despacho) == 0:
      break # finaliza a thread se nao houver encomendas pendentes
    
    
    time.sleep(1)

if __name__ == '__main__':
  
  if len(sys.argv) < 5:
    print('erro')
    sys.exit(1)
  S, C, P, A = map(int, sys.argv[1:])

  if not (P > A > C):
        print('Erro: Os valores devem satisfazer a relação P >> A >> C.')
        print(f'Valores fornecidos: P={P}, A={A}, C={C}')
        print('Certifique-se de que o número de encomendas (P) seja maior que a capacidade de carga (A),')
        print('e que a capacidade de carga (A) seja maior que o número de veículos (C).')
        sys.exit(1)

  entregas_restantes = 10

  # Criação das encomendas
  for i in range(0, int(P)):
    origem = random.randint(0, (int(S) - 1))
    destino = random.randint(0, (int(S) - 1))
    thread = threading.Thread(target=thread_encomenda,args=(i,origem,destino))
    thread.daemon = True
    thread.start()
    threads_encomendas.append(thread)

  # Criação dos pontos
  for i in range(0, int(S)):
    aguardando_despacho = [ encomenda.id for encomenda in encomendas if encomenda.origem == i]
    thread = threading.Thread(target=thread_ponto,args=(i, aguardando_despacho))
    thread.daemon = True
    thread.start()
    threads_pontos.append(thread)

  # Criação dos veículos
  for i in range(0, int(C)):
    ponto_inicial = random.randint(0, int(S))
    thread = threading.Thread(target=thread_veiculo,args=(i, A, ponto_inicial))
    thread.daemon = True
    thread.start()
    threads_veiculos.append(thread)

  monitor = threading.Thread(target=thread_monitor)
  monitor.daemon = True
  monitor.start()

  # Loop Principal que valida interrupções do usuário
  # OBS: pelas threads estarem em modo daemon elas só existem enquanto o main existir, por isso esse loop é necessário
  try:
    while entregas_restantes > 0:
      time.sleep(10)
  except KeyboardInterrupt:
      print("\nEncerrando programa principal.")
  finally:
    programa_ativo = False
    for thread in threads_encomendas + threads_veiculos + threads_pontos:
      thread.join()
    print("Programa finalizado com sucesso")