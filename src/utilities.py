import socket
import colorama
import errno
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


#PURPOSE: Print results of scan
def print_results(port, status_connection):
    
    
    if status_connection == 0:
        status = "OPEN"
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"

        banner = "No banner detected" #TODO sviluppa funzione banner
        print(colorama.Fore.GREEN + f"{port:<9}{status:<12}{service:<17}{banner}" + colorama.Style.RESET_ALL)
    
    elif status_connection in (errno.ECONNREFUSED, 10061):
        status = "CLOSED"
        banner = "   -   "
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
        print(colorama.Fore.RED + f"{port:<9}{status:<12}{service:<14}{banner}" + colorama.Style.RESET_ALL)

    elif status_connection in (errno.ETIMEDOUT, errno.EHOSTUNREACH, 10060, 10035):
        status = "FILTERED"
        banner = "   -   "
        try:
            service = socket.getservbyport(port)
        except:
            service = "unknown"
        print(colorama.Fore.YELLOW + f"{port:<9}{status:<12}{service:<14}{banner}" + colorama.Style.RESET_ALL)

    else:
        status = f"ERROR (Codice: {status_connection})"
        print(status)


#PURPOSE: Scan one single port
def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    connection_result = s.connect_ex((ip, port)) 

    print("\nPORT     STATUS      SERVICE         VERSION")
    print("─────    ────────    ───────         ─────────────────")

    print_results(port, connection_result)
    
    s.close()

#PURPOSE: Save and Parsing Port Range Target inserted by user
def PORT_RANGE_target():
    #Richiede all'utente di inserire un intervallo di porte e restituisce una lista di porte valide
    user_range_input = input(colorama.Fore.CYAN + "[PORT RANGE TARGETS] (ex: 40-1000): " + colorama.Style.RESET_ALL)
    user_ports = user_range_input.split("-")
    first_port = user_ports[0]
    last_port = user_ports[1]
    return first_port, last_port

#PURPOSE: Scan multiple ports
def scan_ports(ip, first, last):

    print("\nPORT     STATUS      SERVICE         VERSION")
    print("─────    ────────    ───────         ─────────────────")

    for port in range(int(first), int(last) + 1):
    #devo creare sempre una nuova socket, una per ogni porta con cui sto cercando di connettermi
        new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_s.settimeout(3)

        connection_result = new_s.connect_ex((ip, port))
        print_results(port, connection_result)
        new_s.close()