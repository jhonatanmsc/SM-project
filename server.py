#coding:utf-8
import socket

def main():

    while True:
        menu = ("--------------MENU-----------\n"
                "1 - Executar como TCP server\n"
                "2 - Executar como UDP server\n"
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
        PACKET_SIZE = 512 if protocol == 'tcp' else 32768                                # Tamanho do Buffer do Pacote
        PROTOCOL = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM

        ptServer = socket.socket(socket.AF_INET, PROTOCOL)
        orig = (HOST, PORT)
        ptServer.bind(orig)
        if protocol == 'tcp':
            ptServer.listen(1)

        print("\nServidor ligado como %s Server em %s:%s" %(protocol.upper(), HOST, PORT))

        total_received = 0
        total_data = 10485760 #10MB in Bytes
        while total_received < total_data:
            if protocol == 'tcp':
                con, cliente = ptServer.accept()
                print ('Conectado por %s : %s' % cliente)
            
            while total_received < total_data:
                if protocol == 'tcp':
                    msg = con.recv(PACKET_SIZE)
                    total_received += PACKET_SIZE
                else:
                    print("I")
                    msg, cliente = ptServer.recvfrom(32768)
                    print("O")
                    total_received += 32768
                if not msg:
                    break
                print(total_received)

            print ('Pacote enviado pelo cliente %s [%s]' %cliente)
            if protocol == 'tcp':
                con.close()
            if protocol != 'tcp':
                ptServer.close()

    except KeyboardInterrupt as e:
        print('\n\n')
        pass

if __name__ == '__main__':
    main()