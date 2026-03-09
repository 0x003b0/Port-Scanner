import socket
import re

#SERVICES THAT SEND BANNER AUTOMATICALLY
#22, 23, 21, 25, 587, 3306, 110, 143 

def _port_21(banner):
    match = re.search(r'\((.+?)\)', banner)
    if match:
        return match.group(1)

#PORT 25: serve dividerlo perchè restituisce '220 kali.kali ESMTP Postfix (Debian)' e a me interessa solo "ESMTP Postfix (Debian)"
def _port_25(banner):
    parts = banner.split(" ", 2) #parts diventerebbe ['220', 'kali.kali', 'ESMTP Postfix (Debian)'] 
    if parts[0].isdigit(): #isdigit() controlla che il primo elemento è un numero, infatti 220 lo è
        return parts[2].strip()
    
def _port_3306(banner):
    banner = repr(banner).strip('"') #rimuove virgolette "" da "F\x00\x00\x00j\x04Host '192.168.1.3' is not allowed to connect to this MariaDB server"
    return banner

def _port_80(s_socket):
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

def _port_6379(s_socket):
    s_socket.send("INFO server\r\n".encode())
    response = s_socket.recv(1024).decode(errors="ignore").strip()
    for line in response.split("\n"):
        if line.lower().startswith("redis_version:"): 
            return line
        
def _port_5901(banner):
    if "RFB" in banner:
        version = banner.split(" ")[1].strip()
        parts = version.split(".")
        return f"VNC (Protocol {int(parts[0])}.{int(parts[1])})" 
    else:
        return "No banner data"

#PURPOSE: Main function to grab the Port Banner
def capture(port, s_socket):
    #services automatically send banner
    try: 
        banner = s_socket.recv(1024).decode(errors="ignore").strip()
        if banner:
            if port == 21:
                return _port_21(banner)
            elif port == 25:
                return _port_25(banner)
            elif port == 3306:
                return _port_3306(banner)
            elif port == 5901:
                return _port_5901(banner)
        return banner
    except socket.timeout:
        pass
    except (OSError, UnicodeDecodeError):
        return "No banner data"
    
    #services do not send banner automatically, need special requests
    try: 
        if port in (80, 8080):
            return _port_80(s_socket)
        elif port == 6379:
            return _port_6379(s_socket)
        else:
            return "No banner data"
    except:
        return "No banner data"