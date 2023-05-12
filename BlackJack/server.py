import random
import socket

def deal_card():
    cards = [1,2,3,4,5,6,7,8,9,10,11,12]
    return random.choice(cards)

def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(player1_score, player2_score):
    if player1_score == player2_score:
        return ""
    elif player2_score == 0:
        return ""
    elif player1_score == 0:
        return ""
    elif player1_score > 21:
        return ""
    elif player2_score > 21:
        return ""
    elif player1_score > player2_score:
        return ""
    else:
        return ""

def receive_player_name():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # VIA UDP 
    host = socket.gethostname()
    port = 12346
    server_socket.bind((host, port))
    print("Aguardando nome do jogador...")

    # recebe o nome do jogador
    player_name, client_address = server_socket.recvfrom(1024)
    player_name = player_name.decode()

    # fecha o socket
    server_socket.close()

    return player_name

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # VIA TCP
    host = socket.gethostname()
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(2)

    print("Aguardando jogadores...")

    # recebe o nome do jogador
    player1_name = receive_player_name()
    player2_name = receive_player_name()

    # aceita as conexões
    player1_socket, player1_address = server_socket.accept()
    print(f"Jogador 1 conectado: {player1_name} ({player1_address})")

    player2_socket, player2_address = server_socket.accept()
    print(f"Jogador 2 conectado: {player2_name} ({player2_address})")

    # começa o jogo
    play_game(player1_name, player1_socket, player2_name, player2_socket)

    # fecha as conexões
    player1_socket.close()
    player2_socket.close()
    server_socket.close()

def play_game(player1_name, player1_socket, player2_name, player2_socket):
    player1_cards = []
    player2_cards = []
    game_over = False

    # inicia o jogo para cada jogador
    for _ in range(2):
        player1_cards.append(deal_card())
        player2_cards.append(deal_card())

    while not game_over:
        # envia as cartas e pontuações para os jogadores
        player1_socket.send(f"{player1_name}, suas cartas: {player1_cards}, pontuação: {calculate_score(player1_cards)}".encode())
        player2_socket.send(f"{player2_name}, suas cartas: {player2_cards}, pontuação: {calculate_score(player2_cards)}".encode())

        # recebe a resposta do jogador 1
        player1_response = player1_socket.recv(1024).decode()

        if player1_response == 's':
            player1_cards.append(deal_card())
            player1_score = calculate_score(player1_cards)
            if player1_score > 21:
                player1_socket.send("Você perdeu. Você ultrapassou 21!".encode())
                player2_socket.send(f"{player1_name} ultrapassou 21! {player2_name} ganhou!".encode())
                game_over = True
        else:
            player1_score = calculate_score(player1_cards)

        # recebe a resposta do jogador 2
        player2_response = player2_socket.recv(1024).decode()

        if player2_response == 's':
            player2_cards.append(deal_card())
            player2_score = calculate_score(player2_cards)
            if player2_score > 21:
                player2_socket.send("Você perdeu. Você ultrapassou 21!".encode())
                player1_socket.send(f"{player2_name} ultrapassou 21! {player1_name} ganhou!".encode())
                game_over = True
        else:
            player2_score = calculate_score(player2_cards)

        # checa se o jogo acabou
        if player1_response == 'n' and player2_response == 'n':
            game_over = True
            result = compare(player1_score, player2_score)
            player1_socket.send(result.encode())
            player2_socket.send(result.encode())

    # fecha as conexões
    player1_socket.close()
    player2_socket.close()

start_server()