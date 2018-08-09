#coding:utf-8
import os
import re
import time
import socket
import platform
import subprocess as sp

def main():
    while True:
        menu = ("\n-----------MENU CLIENTE-----------\n"
                "1 - executar como TCP\n"
                "2 - executar como UDP\n"
                "3 - testar QoS usando TCP\n"
                "4 - testar QoS usando UDP\n"
                "0 - Sair da Aplicação\n"
                )
        op = input(menu + "Informe a opção desejada: ")
        host = input("Informe o endereço do servidor (127.0.0.1 default ): ")
        if host == '':
            host = '127.0.0.1'

        if op == "0":
            print('\n\nAplicação finalizada pelo usuario!!')
            break
        elif op == "1":
            sendFile('tcp')
        elif op == "2":
            sendFile('udp')
        elif op == "3":
            testeQoSTCP('tcp', host)
        elif op == "4":
            testeQoSTCP('udp', host)
        else:
            print("opção invalida")

def sendFile(protocol, host='127.0.0.1'):
    HOST = host
    FILE = 'package-tcp.txt' if protocol == 'tcp' else 'package-udp.txt'
    BASE_FILE = open(FILE, 'r').read()
    PORT = 10000 if protocol == 'tcp' else 10001
    PROTOCOL = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM

    server = socket.socket(socket.AF_INET, PROTOCOL)
    dest = (HOST, PORT)
    server.connect(dest)
    msg = bytes(BASE_FILE, 'utf-8')
    print(type(msg))
    server.send(msg)

    if protocol == 'tcp':
        server.send(msg)                                        # para porta TCP enviaremos 10Mbytes
    else:                                                       # devido ao limite que a porta UDP
        for i in range(100):                                    # pode receber/enviar enviarei 1Mbyte 10 vezes
            server.send(msg)

    server.close()


def testeQoSTCP(protocol, host='127.0.0.1', as_a_dict=False):
    SERVIDOR = host
    print("LOL " + host)
    if isAlive(SERVIDOR):

        try:
            qos_latencia = latencia(SERVIDOR)
            qos_banda = larguraBanda(protocol, SERVIDOR)
            qos_jitter = jitter(SERVIDOR)

        except ConnectionRefusedError:
            print("  conexão recusada. verifique se o servidor TCP está em execução, e se está aceitando conexões.") 

        if not as_a_dict:
            print("\n######## Resultados testes QoS ########\n")
            print("latência(ms): %.4f" %qos_latencia)
            print("banda (Mbits/s): %.2f" %qos_banda)
            print("jitter (ms): %.4f " %qos_jitter)
            print("\n")
            return None
        else:
            return {'latencia':qos_latencia, 'banda':qos_banda, 'jitter':qos_jitter}

    else:
        print("  o host não está acessivel no momento, verifique o endereço, se o host está conectado à rede e tente novamente.")       

def latencia(host='127.0.0.1'): ## este método testa o QoS relativo à latência do meio
    status,result = ("","")
    if platform.system()=="Linux":
        status,result = sp.getstatusoutput("ping -c1 %s "%host)
        time = re.search('time=([0-9]{1,4}\.[0-9]{1,4})',result)
        print(time)
        if time:
            f = time.group(1)
            return float(f)
        return 0.0
    else:
        status,result = sp.getstatusoutput("ping -c1 -w2 %s > nul" %host)
        time = re.search('time=([0-9]{1,4}\.[0-9]{1,4})',result)
        if time:
            f = time.group(1)
            return float(f)
        return 0.0


def larguraBanda(protocol, host='127.0.0.1'): ## este método testa o QoS relativo á largura de banda do meio
    FILE = 'package-tcp.txt' if protocol == 'tcp' else 'package-udp.txt'
    BASE_FILE = open(FILE, 'r').read()
    HOST = host
    print('dota '+host)
    PORT = 10000 if protocol == 'tcp' else 10001
    PROTOCOL = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM

    server = socket.socket(socket.AF_INET, PROTOCOL)
    dest = (HOST, PORT)
    server.connect(dest)
    msg = bytes(BASE_FILE, 'utf-8')
    if protocol == 'tcp':
        init = time.time()
        server.send(msg)
        end = time.time()
    else:
        init = time.time()
        for i in range(100):
            server.send(msg)
        end = time.time()
    
    server.close()
    
    tempo_gasto = (end-init)

    # transmitimos bytes em bites.
    # considerando que a payload de testes foi de 10MBytes, então transmitimos 80Mbits.

    TAXA_MBITS_SEC = 80/tempo_gasto

    return TAXA_MBITS_SEC


def jitter(host='127.0.0.1'): ## este método testa o QoS relativo ao Jitter do meio

    icmp_values = []
    for  i in range(100):
        icmp_values.append(latencia(host))

    menor_valor = min(icmp_values)
    maior_valor = max(icmp_values)

    jitter = maior_valor - menor_valor

    return jitter

def isAlive(host='127.0.0.1'):
    if platform.system()=="Linux":
        status,result = sp.getstatusoutput("ping -c1 %s "%host)
        if status == 0:
            return True
        return False

    else:
        status,result = sp.getstatusoutput("ping -c1 -w2 %s > nul" %host)
        if status == 0:
            return True
        return False

if __name__ == '__main__':
    main()