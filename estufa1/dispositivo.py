import paho.mqtt.client as mqtt
import time
from hal import aquecedor, temperatura, aquecedorLigado
from definitions import usuario, password, client_id, server, port
habilita = True
ligaAquecedor = True

def mensagem(client, user, msg):
    vetor = msg.payload.decode().split(',')
    global habilita
    global ligaAquecedor
    
    # se a mensagem for da habilitação da temperatura
    if msg.topic == f'v1/{usuario}/things/{client_id}/cmd/2':
        habilita = True if vetor[1] == '1' else False
        if habilita:
            print('Temperatura LIGADA')
            client.publish(f'v1/{usuario}/things/{client_id}/data/1', temperatura(ligaAquecedor)[0])
        else:
            print('Temperatura DESLIGADA')
            client.publish(f'v1/{usuario}/things/{client_id}/data/1', '')
    # se a mensagem for do controle do aquecedor    
    if msg.topic == f'v1/{usuario}/things/{client_id}/cmd/3':
        ligaAquecedor = True if vetor[1] == '1' else False    
    
    # envia mensagem de resposta para o botão acionado
    client.publish(f'v1/{usuario}/things/{client_id}/response', f'ok,{vetor[0]}')

# Conexão inicial
client = mqtt.Client(client_id)
client.username_pw_set(usuario, password)  
client.connect(server, port)

# Subscrição dos botões de controle
client.on_message = mensagem
client.subscribe(f'v1/{usuario}/things/{client_id}/cmd/2')
client.subscribe(f'v1/{usuario}/things/{client_id}/cmd/3')
client.loop_start()

# Comportamento do sistema
while True:
    if habilita:
        # recebe o valor da temperatura e se o aquecedor está ligado
        valorTemp, aquecedorLigado = temperatura(ligaAquecedor)
        # publica o valor da temperatura
        client.publish(f'v1/{usuario}/things/{client_id}/data/1', valorTemp)
        if aquecedorLigado:
            # se ligou o aquecedor, acende o led
            client.publish(f'v1/{usuario}/things/{client_id}/data/4', 'On')
        else:
            # senão, apaga o led
            client.publish(f'v1/{usuario}/things/{client_id}/data/4', '')
        time.sleep(5)
    else:
        # desativa todos os dispositivos se não estiver habilitado
        client.publish(f'v1/{usuario}/things/{client_id}/data/1', '')
        client.publish(f'v1/{usuario}/things/{client_id}/data/4', '')
        time.sleep(5)
  
