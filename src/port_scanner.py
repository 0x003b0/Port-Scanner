import colorama
import pyfiglet
import socket

colorama.init()

#Creazione Socket - AF_INET: IPv4, SOCK_STREAM: TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.settimeout(5) #Imposta un timeout di 5 secondi per la connessione

def program_title():
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)


def show_menu():
    print("[1] Scan one single port")
    print("[2] Scan a range of ports")
    print("[3] Exit")
    user_choice = input(colorama.Fore.CYAN + "[CHOOSE AN OPTION]: " + colorama.Style.RESET_ALL)
    return user_choice

program_title()
show_menu()

def IP_target():
    target = input("[IP TARGET]: ")
    if target == "":
        print("Indirizzo IP non valido. Inserisci un indirizzo IP valido.")
        return IP_target() #Richiama la funzione se l'indirizzo IP inserito è vuoto
    return target

def PORT_target():
    port = int(input("[PORT TARGET]: "))
    if port < 1 or port > 65535:
        print("Porta non valida. Inserisci un numero tra 1 e 65535.")
        return PORT_target() #Richiama la funzione se la porta inserita non è valida
    return port

def RANGE_target():
    #Richiede all'utente di inserire un intervallo di porte e restituisce una lista di porte valide
    user_range_input = input(colorama.Fore.CYAN + "[PORT RANGE TARGETS] (ex: 40-1000)" + colorama.Style.RESET_ALL)
    #TODO
    

#Connessione all'Host target
try:
    s.connect((IP_target(), PORT_target()))
    print(colorama.Fore.GREEN + "Connessione stabilita con successo!")
except socket.error:
    print(colorama.Fore.RED + "Connessione fallita. Verifica l'indirizzo IP e la porta del target.")
except socket.timeout:
    print(colorama.Fore.YELLOW + "Connessione scaduta. Il target potrebbe essere offline o la porta è chiusa.")
finally:
    s.close()

#Funzionalità Scanner
#Se la connessione è stabilita, riceviamo lista delle porte
