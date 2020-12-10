#!/usr/bin/env python3

''' Gabriel Jales - Redes de computadores 2020.1: Servidor Token '''

import time
import socket

HOST = '127.0.0.1'  # se conecta ao localhost
PORT = 12345        # porta para se conectar

if __name__ == '__main__':
	print(f'Conectando-se ao servidor {HOST} na porta {PORT}\nPara sair aperte CTRL + C\n ')

	# AF_INET = IPV4, SOCK_STREAM = TCP
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck: # with garante finalizar recursos (não necessita de um .close(), por exemplo)
		# Tratando a conexão também do lado do cliente
		try:
			sck.connect((HOST, PORT)) # conecta-se ao servidor
		except Exception as error:
			raise SystemExit(f'Falha ao conectar-se ao servidor: {HOST} na porta: {PORT}, por que: {error}') # Exceção	
			# Exceção de falha na conexão (porta diferente, por exemplo)
			
		while True: #Loop infinito - receber e enviar dados
			try:
				# Primeira parte: solicita a qtd de tokens e se possível, solicita um token
				sck.send(b'1||-1') # Solicitando qtd de tokens
				data = sck.recv(1024) # recebe dados
				dec_data = data.decode('utf-8').split('||') # formatação dos dados decodificados ('c', 'v'). Split: divide os valores onde tem o separador '||'
				dec_data = dec_data[1] # valor recebido: qtd de tokens disponíveis
				print(f'\n[Servidor] Tokens disponíveis: {dec_data}\n') # Qtd de tokens disponíveis
				
				if int(dec_data) > 0: # se a qtd tokens disponíveis for > 0, solicita um token
					print('--> Solicitando token, aguarde...\n')
					sck.send(b'3||-1') # Protocolo para pedir token ao server
					
				else: # Aguarda para pedir novamente um token (até q esteja disponível 1)
					print('[Servidor]: Aguarde um momento para receber um novo token...\n') 
					time.sleep(7) # tempo de espera
					continue # interrompe a execução do ciclo, sem quebrar o laço (retorna ao início)
				
				# Segunda parte: receber e depois devolver o token
				data = sck.recv(1024)
				dec_data = data.decode('utf-8').split('||')
				dec_data = dec_data[1] # valor: Token
				if (dec_data == '-1'): # '4','-1'
					print('[Servidor]: Recurso indisponível :/ \n')
					continue
				else:
					print(f'\n[Servidor] Token: {dec_data}\n')
					received_token = dec_data # token recebido
					print('Devolvendo token ao servidor, aguarde...')
					time.sleep(3)
					sck.send(f'5||{received_token}'.encode()) # devolução do token
					print('\n[Servidor]: Token recebido!')
					time.sleep(2)
			
			except KeyboardInterrupt: # exceção: ctrl c
				print('\n--> Desconectado!')
				break
