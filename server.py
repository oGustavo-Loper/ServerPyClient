import socket
import threading
import time
import datetime
import os
import socket as s
import platform

senha = 'teste'
usuario = 'Vaniel'
arquivo_para_gravar_saida_diretorio = 'saída_diretorio.txt'
data_hora = datetime.datetime.now()
data = (" %02d/%02d/%04d" % (data_hora.day, data_hora.month, data_hora.year))
hora = (" %02d:%02d" % (data_hora.hour, data_hora.minute))
conexoes = []
pacotes = []

SERVER_IP = "localhost"
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

host = 'localhost'
ip = s.gethostbyname(host)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def ping(host):
    print("---------------------------------------------PINGANDO---------------------------------------------")
    parametrosPingM = "-c 4"
    parametrosPingW = "-n 4"
    if (platform.system().lower() == "windows"):
        ping_str = parametrosPingW
    else:
        ping_str = parametrosPingM
    linhaExecucao = os.system("ping " + ping_str + " " + host)
    retornoping = linhaExecucao
    return retornoping


def enviar_pacote_separado(conexao):
    print(f"[ENVIANDO] Enviando pacote para {conexao['addr']}")
    for i in range(conexao['last'], len(pacotes)):
        mensagem_de_envio = "msg=" + pacotes[i]
        conexao['conn'].send(mensagem_de_envio.encode())
        conexao['last'] = i + 1
        time.sleep(0.2)


def enviar_pacote_todos():
    global conexoes
    for conexao in conexoes:
        enviar_pacote_separado(conexao)


def clientes(conn, addr):
    print(f" Um novo user acabou de se conectar pelo endereço {addr}")
    global conexoes
    global pacotes
    nome = False

    while (True):
        msg = conn.recv(1024).decode(FORMAT)
        if (msg):
            if (msg.startswith("nome=")):
                mensagem_separada = msg.split("=")
                nome = mensagem_separada[1]
                mapa_da_conexao = {
                    "conn": conn,
                    "addr": addr,
                    "nome": nome,
                    "last": 0
                }
                conexoes.append(mapa_da_conexao)
                enviar_pacote_separado(mapa_da_conexao)
            elif (msg.startswith("msg=")):
                mensagem_separada = msg.split("=")
                pacote = nome + "=" + mensagem_separada[1]
                pacotes.append(pacote)
                enviar_pacote_todos()


def start():
    print(" Socket Sendo Iniciada ")
    server.listen()
    while (True):
        conn, addr = server.accept()
        thread = threading.Thread(target=clientes, args=(conn, addr))
        thread.start()


while True:
    file = open(arquivo_para_gravar_saida_diretorio, "w")
    print('##### Seja Bem Vindo #####')
    usuario2 = input('Digite seu Usuario: ')
    pwd = input('Digite sua Senha: ')
    contador_pwd_fail = 0
    while (senha != pwd or usuario != usuario2):
        if contador_pwd_fail == 2:
            exit()
        else:
            print(' Usuario ou Senha Incorreta')
            contador_pwd_fail = contador_pwd_fail + 1
            usuario2 = input('Digite seu Usuario: ')
            pwd = input('Digite sua Senha:')
    print("Login Realizado com Sucesso em", data, hora)
    print("...Carregando Diretório...")
    print(" ")
    cwd = os.getcwd()
    print("Diretorio Atual =", cwd)

    print("ping:", ping('localhost'))
    file.writelines(cwd)
    file.close()

    start()
