#coding:utf-8
import socket

def main():

    while True:
        menu = ("--------------MENU-----------\n"
                "1 - Executar como TCP server\n"
                "2 - Executar como UDP server\n"
                "3 - Executar como TCP e UDP server\n"
                "0 - sair da aplicação\n"
                )
        op = input(menu + "Qual a opção desejada?_")

        if op == "0":
            print('\n\nAplicação finalizada pelo usuario!!')
            break
        elif op == "1":
            server('tcp')
        elif op == "2":
            server('udp')
        else:
            print("opção invalida!!!")


def server(protocol):
    try:
        HOST = '0.0.0.0'        
        PORT = 10000 if protocol == 'tcp' else 10001
        PACKET_SIZE = 512                                               # Tamanho do Buffer do Pacote
        PROTOCOL = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM

        ptServer = socket.socket(socket.AF_INET, PROTOCOL)
        orig = (HOST, PORT)
        ptServer.bind(orig)
        if protocol == 'tcp':
            ptServer.listen(1)

        print("\nServidor ligado como %s Server em %s:%s" %(protocol.upper(), HOST, PORT))
        
        while True:
            if protocol == 'tcp':
                con, cliente = ptServer.accept()
                print ('Conectado por %s : %s' % cliente)
            total_received = 0
            total_data = 10485760 #10MB in Bytes

            while total_received <= total_data:
                if protocol == 'tcp':
                    msg = con.recv(PACKET_SIZE)
                else:
                    msg, cliente = ptServer.recvfrom(PACKET_SIZE)
                if not msg:
                    break
                print(msg)
                total_received += PACKET_SIZE

            print ('Pacote enviado pelo cliente %s [%s]' %cliente)
            con.close() if protocol == 'tcp' else ptServer.close()

    except KeyboardInterrupt as e:
        print('\n\n')
        pass

if __name__ == '__main__':
    main()