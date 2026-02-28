import socket
import colorama
import banner_grabbing

#PURPOSE: Save IP Address Target inserted by user
def IP_target():
    target = input(colorama.Fore.CYAN + "[IP TARGET]: " + colorama.Style.RESET_ALL)
    if target == "":
        print("Indirizzo IP non valido. Inserisci un indirizzo IP valido.")
        return IP_target() #Richiama la funzione se l'indirizzo IP inserito è vuoto
    return target

#PURPOSE: Save Port Target inserted by user
def PORT_target():
    port = int(input(colorama.Fore.CYAN + "[PORT TARGET]: " + colorama.Style.RESET_ALL))
    if port < 1 or port > 65535:
        print("Porta non valida. Inserisci un numero tra 1 e 65535.")
        return PORT_target() #Richiama la funzione se la porta inserita non è valida
    return port

#PURPOSE: Scan one single port and print result
#REVIEW: Questo codice stampa anche i risultati, dovrebbe essere una funzione a parte!
def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    try:
        s.connect((ip, port))
        print(colorama.Fore.GREEN + f"Port {port} is open")
    except socket.error:
        print(colorama.Fore.RED + f"Port {port} is close")
    except socket.timeout:
        print(colorama.Fore.YELLOW + "Connection timed out. The target may be offline or the port may be filtered or closed.")
    finally:
        s.close()

#PURPOSE: Save and Parsing Port Range Target inserted by user
def PORT_RANGE_target():
    #Richiede all'utente di inserire un intervallo di porte e restituisce una lista di porte valide
    user_range_input = input(colorama.Fore.CYAN + "[PORT RANGE TARGETS] (ex: 40-1000): " + colorama.Style.RESET_ALL)
    user_ports = user_range_input.split("-")
    first_port = user_ports[0]
    last_port = user_ports[1]
    return first_port, last_port

#PURPOSE: Scan multiple ports and print results
#REVIEW: Questo codice stampa anche i risultati, dovrebbe essere una funzione a parte!
def scan_ports(ip, first, last):

    print("\nPORT     STATUS      SERVICE         VERSION")
    print("─────    ──────      ───────         ─────────────────")

    for port in range(int(first), int(last) + 1):
    #devo creare sempre una nuova socket, una per ogni porta con cui sto cercando di connettermi
        new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_s.settimeout(1)

        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
            
        try:
            new_s.connect((ip, port))
            status = "OPEN"
            try:
                #TODO:Sviluppare funzione banner
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