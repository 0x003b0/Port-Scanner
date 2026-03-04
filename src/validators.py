import ipaddress
import socket

#PURPOSE: Validate IP Address inserted by user
def is_valid_ip(addr):
    try:
        ipaddress.ip_address(addr) #Controllo che che l'IP inserito sia un indirizzo IP valido
        return True
    except Exception:
        return False

#PURPOSE: Validate Domain Name inserted by user
def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False
    
#PURPOSE: Validate port range inserted by user
def is_valid_range(port1, port2):
    if (1 <= port1 <= 65535) and (1 <= port2 <= 65535) and (port1 <= port2):
        return True
    else:
        return False