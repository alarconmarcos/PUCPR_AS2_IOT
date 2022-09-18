import paho.mqtt.client as mqtt
import time
from hal import temperatura, aquecedor
from definitions import usuario, password, client_id, server, port


def mensagem(client, user, msg):
    vetor = msg.payload.decode().split(',')
    aquecedor('on' if vetor[1] == '1' else 'off')
    client.publish(f'v1/{usuario}/things/{client_id}/response', f'ok,{vetor[0]}')
    print(vetor)

# Conexão inicial
estufa1 = mqtt.Client(client_id)
estufa1.username_pw_set(usuario, password)  
estufa1.connect(server, port)

estufa1.on_message = mensagem
estufa1.subscribe(f'v1/{usuario}/things/{client_id}/cmd/1')
estufa1.loop_start()

# Comportamento do sistema
while True:
    estufa1.publish(f'v1/{usuario}/things/{client_id}/data/0', temperatura())
    time.sleep(10)
  
# client.disconnect()