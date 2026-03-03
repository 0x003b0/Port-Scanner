import socket
import colorama
import errno
import ipaddress
import banner_grabbing

#PURPOSE: Check if IP Address inserted by user is valid
def is_valid_ip(addr):
    try:
        ipaddress.ip_address(addr) #Controllo che che l'IP inserito sia un indirizzo IP valido
        return True
    except:
        return False

#PURPOSE: Check is domain name iserted by user is valid
def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except:
        return False

#PURPOSE: Save One IP Address Target inserted by user
def IP_target():
    while True:
        target = input(colorama.Fore.CYAN + "[IP / DOMAIN TARGET]: " + colorama.Style.RESET_ALL).strip() #strip() è per rimuovere spazi prima e dopo l'input nel caso ci fossero
        if target: #se ha inserito qualcosa, allora esegue il codice dentro l'if
            if is_valid_ip(target) or is_valid_domain(target):
                return target
            else:
                print(colorama.Fore.RED + "[ERROR] Invalid IP Address or domain name.\n")
                continue
        print(colorama.Fore.RED + "[ERROR] IP Address value cannot be empty.\n")

#PURPOSE: Save Port Target inserted by user
def PORT_target():
    while True:
        try:
           port = int(input(colorama.Fore.CYAN + "[PORT TARGET]: " + colorama.Style.RESET_ALL))
           if port >= 1 and port <= 65535:
               return port
           else:
               print(colorama.Fore.RED + "[ERROR] Invalid port. Please enter a number between 1 and 65535\n")
        except:
            print(colorama.Fore.RED + "[ERROR] Port value cannot be empty.\n")

#PURPOSE: Print results of a scan
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

    print("\nPORT     STATE       SERVICE         VERSION")
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

    print("\nPORT     STATE       SERVICE         VERSION")
    print("─────    ────────    ───────         ─────────────────")

    for port in range(int(first), int(last) + 1):
    #devo creare sempre una nuova socket, una per ogni porta con cui sto cercando di connettermi
        new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_s.settimeout(3)

        connection_result = new_s.connect_ex((ip, port))
        print_results(port, connection_result)
        new_s.close()