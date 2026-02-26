import colorama
import pyfiglet
import socket
import sys
import utilities

colorama.init()

#Creating Socket - AF_INET: IPv4, SOCK_STREAM: TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

def program_title():
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)
    print("=" * 50)
    print("Version: 0.1.0")
    print("Purpose: Educational Tool")
    print("Author: 0x003b0")
    print("Github: https://github.com/0x003b0")
    #tool-type: network, cybersecurity tool....
    print("=" * 50)

def show_menu():
    print("\n[1] Scan a specific port")
    print("[2] Scan a range of ports")
    print("[3] Exit\n")

program_title()
show_menu()
user_choice = int(input(colorama.Fore.CYAN + "[>]: " + colorama.Style.RESET_ALL))

if user_choice == 1:
    ip = utilities.IP_target()
    port = utilities.PORT_target()

    #Connessione all'Host target
    try:
        s.connect((ip, port))
        #print(colorama.Fore.GREEN + "Connessione stabilita con successo!")
        print(colorama.Fore.GREEN + f"Port {port} is open" + colorama.Style.RESET_ALL)
    except socket.error:
        print(colorama.Fore.RED + f"Port {port} is close" + colorama.Style.RESET_ALL)
    except socket.timeout:
        print(colorama.Fore.YELLOW + "Connessione scaduta. Il target potrebbe essere offline o la porta è chiusa." + colorama.Style.RESET_ALL)
    finally:
        s.close()  

elif user_choice == 2:
    ip_target = utilities.IP_target()
    utilities.RANGE_target(ip_target)

elif user_choice == 3:
    print('Exiting...')
    sys.exit()

else:
    print('Select 1, 2, or 3')
    sys.exit()