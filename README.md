# [Servidor Token (Thread)]
## Redes de Computadores UERN - 2020

### Passo a passo

#### 1. Rode o servidor e defina o número de tokens disponíveis:
```console
$ python3 server.py
```
#### 2. Em outra janela do terminal, rode também o cliente:
```console
$ python3 client.py
```
> Como esse código utiliza thread, é possível rodar mais de uma instância do cliente (1 server - n clients)

#### Protocolos:

| Código | Valor | Significado                             |   |   |
|--------|-------|-----------------------------------------|---|---|
| 1      | -1    | Cliente solicita quantidade de recursos |   |   |
| 2      | X     | Servidor informa a quantidade X de      |   |   |
| 3      | -1    | Cliente solicita Token                  |   |   |
| 4      | X     | Servidor fornece Token X                |   |   |
| 4      | -1    | Recurso não disponível                  |   |   |
| 5      | X     | Cliente devolve Token X                 |   |   |

