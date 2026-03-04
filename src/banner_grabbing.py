import socket


#codice banner grabbing
    #per farlo bene, va fatto personalizzato, quindi creare richieste diverse a seconda del servizio associato alla porta
    #inziamo con le top 10:
    #1. WEB: 80,443, 8080, 8443
    #2. ACCESSO REMOTO: 22(SSH), 23(Telnet)
    #3. MAIL: 25, 110, 143, 587
    #4. DATABASE: 3306(MySQL), 5432(Postgres)
    #5. FILE SHARING: 21(FTP), 445(SMB)
    #6. INDUSTRIA/IoT: 502(Modbus), 1883(MQTT)

    #QUALI DI QUESTI INVIANO BANNER AUTOMATICAMENTE?
    #22, 23, 21, 25, 587, 3306, 110, 143 

    ###################################################################################################
    #PORTA 80
    ###################################################################################################
        #PER RICEVERE IL BANNER, CON ALCUNI SERVIZI FUNZIONA SEMPLICEMENTE IL banner = s.recv(1024) MA PER ALTRI NO, DEVI INVIARE UN RICHIESTA TU!
        #request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
        #s.send(request.encode())



# def banner_grabbing(ip, port, socket_input):
#     banner = socket_input.recv(1024).decode().strip()
#     try: #se servizio invia automaticamente banner
#         banner = s.recv(1024).decode().split()
#         print(banner)
#     except socket.error: #se il servizio richiede una richiesta per inviarti il banner
#         s.send(b"HELP\r\n\r\n") #perchè scritto cosi?
#         banner = s.recv(1024).decode().split()
#         print(banner)
#     except socket.timeout:
#         s.send(b"HELP\r\n\r\n") #perchè scritto cosi?
#         banner = s.recv(1024)
#         print(banner)

#     print(banner)