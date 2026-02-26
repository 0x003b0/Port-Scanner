import socket
import colorama

def IP_target():
    target = input(colorama.Fore.CYAN + "[IP TARGET]: " + colorama.Style.RESET_ALL)
    if target == "":
        print("Indirizzo IP non valido. Inserisci un indirizzo IP valido.")
        return IP_target() #Richiama la funzione se l'indirizzo IP inserito è vuoto
    return target

def PORT_target():
    port = int(input(colorama.Fore.CYAN + "[PORT TARGET]: " + colorama.Style.RESET_ALL))
    if port < 1 or port > 65535:
        print("Porta non valida. Inserisci un numero tra 1 e 65535.")
        return PORT_target() #Richiama la funzione se la porta inserita non è valida
    return port

def RANGE_target(ip_target_input):
    #Richiede all'utente di inserire un intervallo di porte e restituisce una lista di porte valide
    user_range_input = input(colorama.Fore.CYAN + "[PORT RANGE TARGETS] (ex: 40-1000): " + colorama.Style.RESET_ALL)
    user_ports = user_range_input.split("-")
    first_port = user_ports[0]
    last_port = user_ports[1]

    #conversione da str a int perchè senno il ciclo non funziona (range prende solo interi)

    print("\nPORT     STATUS      SERVICE         VERSION")
    print("─────    ──────      ───────         ─────────────────")

    #ora deve scan le porte inserite dall'utente
    for port in range(int(first_port), int(last_port)):
        #intenta connessione su ogni porta; devo creare sempre una nuova socket, una per ogni porta con cui sto cercando di connettermi
        new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_s.settimeout(1)
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
            
        try:
            new_s.connect((ip_target_input, port))
            status = "OPEN"
            
            try:
                banner = new_s.recv(1024).decode().strip()
            except:
                banner = "No banner detected"

            print(colorama.Fore.GREEN + f"{port:<9}{status:<12}{service:<17}{banner}" + colorama.Style.RESET_ALL)

        except socket.error:
            status = "CLOSED"
            banner = "   -   "
            print(colorama.Fore.RED + f"{port:<9}{status:<12}{service:<14}{banner}" + colorama.Style.RESET_ALL)
            
        except socket.timeout:
            status = "TIMEOUT/FILTERED"

            try:
                banner = new_s.recv(1024).decode.strip()
            except:
                banner = "No banner detected"

            print(colorama.Fore.YELLOW + f"{port:<9}{status:<12}{service:<12}{banner}" + colorama.Style.RESET_ALL)
        finally:
            new_s.close()