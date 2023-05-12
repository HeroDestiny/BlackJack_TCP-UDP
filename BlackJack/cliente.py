import socket

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # CONEXÃO VIA TCP
    host = socket.gethostname()
    port = 12345
    client_socket.connect((host, port))
    return client_socket

def send_player_name(player_name):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ENVIO VIA UDP
    host = socket.gethostname()
    port = 12346
    server_socket.sendto(player_name.encode(), (host, port))
    server_socket.close()

def play_game(client_socket):
    while True:
        # recebe e mostra as cartas e a pontuação do jogador
        response = client_socket.recv(1024).decode()
        print(response)

        # confirma se o jogo acabou
        if "ganhou" in response or "perdeu" in response or "Empate" in response:
            break

        choice = input("Deseja pegar mais uma carta? (s/n): ")
        client_socket.send(choice.encode())

    # recebe e mostra o resultado
    result = client_socket.recv(1024).decode()
    print(result)

    client_socket.close()

# connecta ao server
client_socket = connect_to_server()
print("Conectado ao servidor.")

# recebe o nome do jogador
player_name = input("Digite o seu nome: ")

# envia os nomes ao servidor
send_player_name(player_name)

# começa o jogo
play_game(client_socket)
