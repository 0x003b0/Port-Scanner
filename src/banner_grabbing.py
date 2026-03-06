import socket

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
#PORTA 21 - FTP (Automatico) - ?
#PORTA 22 - SSH (Automatico) - OK
#PORTA 23 - Telnet (Automatico) - ?
#PORTA 25 - SMTP (Automatico) - ?
#PORTA 110 - POP3 (Automatico) - ?
#PORTA 143 - IMAP (Automatico) - ?
#PORTA 587 - unknown (Automatico) - ?
#PORTA 3306 - unknown (Automatico) - ?
###################################################################################################
def capture(port, s_socket):
    #TRY Nº1 -- SE RICEVE INFO AUTOMATICAMENTE ESEGUE QUESTO TRY
    try: 
        banner = s_socket.recv(1024).decode(errors="ignore").strip()
        if banner:
            return banner
    except socket.timeout:
        pass #cosa fa questo pass?
    except:
        return "No banner data"

    #TRY Nº2 -- SE NON RICEVE INFO AUTOMATICAMENTE ESEGUE QUESTO TRY
    try: 
        if port in (80, 443):
            s_socket.send("GET / HTTP/1.0\r\n\r\n".encode())
            response =  s_socket.recv(1024).decode(errors="ignore")

            #response è del tipo:
            #HTTP/1.0 200 OK\nDate: Fri...\nServer: gws\nX-XSS-Protection...
            #devo cercare di prendere la riga con "Server:...."
            #spezzo tutto in righe dato che La risposta HTTP è una stringa unica 
            # con tutte le righe separate da \n:
            #.split("\n")
            # [
            #     "HTTP/1.0 200 OK",
            #     "Date: Fri...",
            #     "Server: gws",
            #     "X-XSS-Protection: 0",
            #     ...
            # ]
            for line in response.split("\n"): #split divide la stringa usando \n come separatore
                if line.lower().startswith("server:"): 
                    return line.split(":")[1].strip() #prende la linea "Server: gws" con split divide la stringa in [Server, gws] e prende il secondo elemento [1] ovvero gws e leva gli spazi con strip()
        
            return "No banner data"
        else:
            return "No banner data"
    except:
        return "No banner data"























    ###################################################################################################
    #PORTA 80
    ###################################################################################################
        #PER RICEVERE IL BANNER, CON ALCUNI SERVIZI FUNZIONA SEMPLICEMENTE IL banner = s.recv(1024) MA PER ALTRI NO, DEVI INVIARE UN RICHIESTA TU!
