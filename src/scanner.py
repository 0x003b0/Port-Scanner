import socket
import output

#PURPOSE: Create new socket
def _create_new_socket():
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.settimeout(5)
    return new_socket

#PURPOSE: Scan one single port / Create connection with single port
def scan_port(ip, port):
    s = _create_new_socket()
    connection_result = s.connect_ex((ip, port)) 

    output.print_scanner_header()
    output.print_results(port, connection_result, s)

    s.close() #REVIEW:con l'istruzione with si elimina questa riga, chiudendo automaticamente la socket, mettila più avanti

#PURPOSE: Connect to a single port and display result
def _scan_single(ip, port):
    """Connect to a single port and display result"""
    new_s = _create_new_socket()
    connection_result = new_s.connect_ex((ip, port))
    output.print_results(port, connection_result, new_s)
    new_s.close()
        
#PURPOSE: Scan multiple ports in range / Creare multiple connection with ports
def scan_port_range(ip, first, last):
    output.print_scanner_header()
    for port in range(first, last + 1):
    #devo creare sempre una nuova socket, una per ogni porta con cui sto cercando di connettermi
        _scan_single(ip, port)

#PURPOSE: Scan different ports
def scan_ports(ip, list_of_ports):
    output.print_scanner_header()
    #per ogni elemnto della lista, crea una nuova socket
    for port in list_of_ports:
        _scan_single(ip, int(port))
