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
    except Exception:
        return False

#PURPOSE: Check is domain name iserted by user is valid
def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

#PURPOSE: Ask user for IP Address or Domain target
def get_IP_target():
    while True:
        target = input(colorama.Fore.CYAN + "[IP / DOMAIN TARGET]: " + colorama.Style.RESET_ALL).strip() #strip() rimuove spazi prima e dopo l'input
        if target: #se ha inserito qualcosa, allora esegue il codice dentro l'if
            if is_valid_ip(target) or is_valid_domain(target):
                return target
            else:
                print(colorama.Fore.RED + "[ERROR] Invalid IP Address or domain name.\n")
                continue
        print(colorama.Fore.RED + "[ERROR] IP Address value cannot be empty.\n")

#PURPOSE: Ask user for Port target
def get_port_target():
    while True:
        try:
           port = int(input(colorama.Fore.CYAN + "[PORT TARGET]: " + colorama.Style.RESET_ALL))
           if 1 <= port <= 65535:
               return port
           else:
               print(colorama.Fore.RED + "[ERROR] Invalid port. Please enter a number between 1 and 65535.\n")
        except ValueError:
            print(colorama.Fore.RED + "[ERROR] Invalid format. Use <port> (e.g. 80).\n")

#PURPOSE: Return/get Port Service
def get_port_service(port):
    try:
        return socket.getservbyport(port)
    except Exception:
        return "unknown"

#PURPOSE: Print results of a scan
def print_results(port, status_connection):
    if status_connection == 0:
        status = "OPEN"
        service = get_port_service(port)
        banner = "No banner detected"
        print(colorama.Fore.GREEN + f"{port:<9}{status:<12}{service:<17}{banner}" + colorama.Style.RESET_ALL)
    elif status_connection in (errno.ECONNREFUSED, 10061):
        status = "CLOSED"
        banner = "   -   "
        service = get_port_service(port)
        print(colorama.Fore.RED + f"{port:<9}{status:<12}{service:<14}{banner}" + colorama.Style.RESET_ALL)
    elif status_connection in (errno.ETIMEDOUT, errno.EHOSTUNREACH, 10060, 10035):
        status = "FILTERED"
        banner = "   -   "
        service = get_port_service(port)
        print(colorama.Fore.YELLOW + f"{port:<9}{status:<12}{service:<14}{banner}" + colorama.Style.RESET_ALL)
    else:
        status = f"ERROR (Codice: {status_connection})"
        print(status)

#PURPOSE: Print Scanner Header results
def print_scanner_header():
    print("\nPORT     STATE       SERVICE         VERSION")
    print("─────    ────────    ───────         ─────────────────")

#PURPOSE: Create new socket
def create_new_socket():
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.settimeout(3)
    return new_socket

#PURPOSE: Scan one single port / Create connection with single port
def scan_port(ip, port):
    s = create_new_socket()
    connection_result = s.connect_ex((ip, port)) 

    print_scanner_header()

    print_results(port, connection_result)
    s.close() #REVIEW:con l'istruzione with si elimina questa riga, chiudendo automaticamente la socket, mettila più avanti

#PURPOSE: Check if ports inserted are in [1-65535]
def is_valid_range(port1, port2):
    if (1 <= port1 <= 65535) and (1 <= port2 <= 65535) and (port1 <= port2):
        return True
    else:
        return False

#PURPOSE: Ask user for a Port Range Target
def get_port_range_target():
    while True:
        user_range_input = input(colorama.Fore.CYAN + "[PORT RANGE TARGETS] (e.g.: 40-1000): " + colorama.Style.RESET_ALL).strip()

        try:
            user_ports = user_range_input.split("-")

            if len(user_ports) != 2: #nel caso scrivesse 10-20-22 invece di 10-20
                raise ValueError

            first_port = int(user_ports[0])
            last_port = int(user_ports[1])

            if is_valid_range(first_port, last_port):
                return first_port, last_port
            else:
                print(colorama.Fore.RED + "[ERROR] Invalid port range. Valid ports must be between 1 and 65535.\n")

        except (ValueError, IndexError):
            print(colorama.Fore.RED + "[ERROR] Invalid format. Use: <start>-<end> (e.g. 40-100).\n")
        
#PURPOSE: Scan multiple ports
def scan_ports(ip, first, last):
    print_scanner_header()

    for port in range(first, last + 1):
    #devo creare sempre una nuova socket, una per ogni porta con cui sto cercando di connettermi
        new_s = create_new_socket()
        connection_result = new_s.connect_ex((ip, port))
        print_results(port, connection_result)
        new_s.close()