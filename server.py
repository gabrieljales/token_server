#!/usr/bin/env python3

''' Gabriel Jales - Redes de computadores 2020.1: Servidor Token '''

import socket 
import secrets
import random 
from threading import Thread   

#HOST = ''    # Em branco, escuta qualquer endereço
#HOST = 'site.org'  # Escuta o endereço que tenha esse hostname
HOST = '127.0.0.1'              # Escuta somente o localhost
PORT = 12345           # 1-65535 (usar acima de 1023)

def generate_tokens(num_tokens): # Função para gerar tokens
	#num_tokens = random.randrange(10) # gerar token sem input (automático)
	token_list = [] # Lista para armazenar tokens gerados
	for i in range(0, num_tokens):
		token = secrets.token_urlsafe(20) # Gerando token utilizando o método token_urlsafe
		token_list.append(token) # Adicionando token à lista
	return token_list # Retorna a lista de tokens

def get_token(target_list, destination_list):
	random_token = random.choice(target_list) # pega um token aleatório com o método .choice() da lista alvo
	target_list.remove(random_token) # Remove da lista inicial
	destination_list.append(random_token) # Adiciona na lista de destino
	return random_token # retorna o token aleatório

def manage_connection(client, connection): # Função para gerir conexões
	print(f'\n--> Uma nova conexão foi feita! Endereço: {connection[0]}, Porta: {connection[1]}\n')
	client_tokens = [] #Lista de tokens do cliente (cada um tem a sua)
	
	while True:  # loop para receber e enviar dados
		message = client.recv(1024)     # recebendo a mensagem - Até 1024 bytes (formato recebido: 'cod||val')
		code_value = [] # Lista para armazenar código e valor recebidos na msg 
		code_value.append((message.decode()).split("||", 1)) # Separa o código e o valor no formato: ['c','v'], remove o separador '||'  
		# Append da mensagem decodificada e sem o separador          
		
		if not message: # quando o cliente encerra a conexão (ctrl + c)
			print(f'\n--> Conexão encerrada - Endereço: {connection[0]}, Porta: {connection[1]}\n')
			break # quebra o loop
		
		# Protocolos
		if code_value[0][0] == '1' and code_value[0][1] == '-1': # protocolo: '1','-1'
			print(f'[Cliente {connection[1]}]: Solicitou a quantidade de recursos disponíveis\n')
			resp = ['2', str(len(server_tokens))] # '2', 'qtd_tokens'
			response = "||".join(resp) # reposta: '2||qtd_tokens'
			client.sendall(response.encode('utf-8')) # Enviando resposta para o client (bytes)
			
		elif code_value[0][0] == '3' and code_value[0][1] == '-1': # protocolo: '3','-1'
			if len(server_tokens) > 0: # caso tenha tokens disponíveis no server...
				print(f'[Cliente {connection[1]}]: Solicitou um token\n--> Aguardando devolução do token...\n')
				token = get_token(server_tokens, client_tokens) # pega um token do servidor e manda para o cliente (armazena em uma var para saber qual foi o token)
				resp2 = ['4', token] # '4', 'token'
				response2 = "||".join(resp2) # Resposta: '4||token'
				client.sendall(response2.encode('utf-8')) # Envia para o cliente (bytes)
				print(f'\n--> SERVER TOKENS = {server_tokens}') # Visualizar tokens do server
				print(f'\n--> CLIENT [{connection[1]}] TOKENS = {client_tokens}\n') # Visualizar tokens do client
				
			else: # protocolo: 4||-1
				resp2 = ['4', '-1'] # '4', '-1'
				response2 = "||".join(resp2) # resposta: '4||-1'
				client.sendall(response2.encode('utf-8')) # Envia para o cliente
				
		elif code_value[0][0] == '5': # protocolo '5','token'
			token = get_token(client_tokens, server_tokens) # retira token do cliente, devolve ao server
			print(f'[Cliente {connection[1]}]: Devolveu o token "{token}".\n')
			print(f'\n--> SERVER TOKENS = {server_tokens}') # Visualizar tokens do server
			print(f'\n--> CLIENT [{connection[1]}] TOKENS = {client_tokens}\n') # Visualizar tokens do client
	
	client.close()      # encerrando a conexão se o loop for quebrado

if __name__ == '__main__':
	token_choice = int(input('Digite a quantidade de tokens para serem disponibilizados aos clientes: \n--> ')) # configura qtd de tokens do server
	server_tokens = generate_tokens(token_choice) # gera a lista a partir do número de tokens, e armazena em server_tokens
	print(f'--> Qtd de tokens disponíveis: {len(server_tokens)}\n')
	
	print(f'\nRodando o servidor em {HOST} na porta {PORT}\n--> Aguardando conexão...\n')
	
	sck = socket.socket()                 # Criando o socket (instância)
	sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Flag para evitar o erro "Address already in use" (reutiliza a porta)

	try:
		sck.bind((HOST, PORT))                # atribui um endereço IP e um número de porta a uma instância de soquete. (vinculou o host e a porta com o socket)
		sck.listen()                         # Começa a escutar (socket em estado de 'escuta')
	except socket.error as error: # Tratar erros relacionados ao socket
		raise SystemExit(f'Falha ao conectar-se ao servidor: {HOST} na porta: {PORT}, por que: {error}') #raise chama a exceção, systemExit encerra o script 
		# Exceção de falha na conexão (porta diferente, por exemplo)

	while True: # loop de conexões (cada uma em um thread paralela)
		try:
			client, connection = sck.accept()               # aceitar / bloquear e esperar por novas conexões
			t = Thread(target=manage_connection, args=(client, connection))  # cria uma nova thread
			t.start()                             # Iniciando thread
		except KeyboardInterrupt:
			print('\n--> Servidor encerrado!')
			break
		except socket.error as error:
			print(f'--> Não foi possível conectar-se ao servidor, pois {error}')
	sck.close() # encerrando a conexão se o laço for quebrado
