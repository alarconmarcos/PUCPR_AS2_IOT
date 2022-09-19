import string

valorTemp = 30
aquecedorLigado = False

# função de ler a temperatura
def temperatura(ligaAquecedor: bool):
    global valorTemp
    global aquecedorLigado
    
    if (valorTemp < 25) and (ligaAquecedor):
        aquecedor(True)
    if valorTemp > 30:
        aquecedor(False)
    if aquecedorLigado:   
        valorTemp += 1
    else:
        valorTemp -= 1
    return [valorTemp, aquecedorLigado] #recebe o valor da temperatura e se o aquecedor está ligado

# função de ligar o aquecedor        
def aquecedor(ligado: bool):
    global aquecedorLigado
    if ligado:
        aquecedorLigado = True
        print('Aquecedor LIGADO')
    else:
        aquecedorLigado = False
        print('Aquecedor DESLIGADO')