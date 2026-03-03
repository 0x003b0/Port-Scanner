import colorama
import pyfiglet
import socket
import sys
import utilities

colorama.init(autoreset=True)

#PURPOSE: Show program title
def program_title():
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)
    print("=" * 50)
    print("Version: 0.1.0")
    print("Purpose: Educational Tool")
    print("Author: 0x003b0")
    print("Github: https://github.com/0x003b0")
    print("=" * 50)

#PURPOSE: Show menu for user
def show_menu():
    print("\n[1] Scan a specific port")
    print("[2] Scan a range of ports")
    print("[3] Exit\n")

program_title()
show_menu()

#PURPOSE: Menu user choise
user_choice = int(input(colorama.Fore.CYAN + "[>]: " + colorama.Style.RESET_ALL))

if user_choice == 1:
    ip = utilities.get_IP_target()
    port = utilities.get_port_target()
    utilities.scan_port(ip,port)

elif user_choice == 2:
    ip = utilities.get_IP_target()
    first_port, last_port = utilities.get_port_range_target()
    utilities.scan_ports(ip, first_port, last_port)

elif user_choice == 3:
    print('Exiting...')
    sys.exit()

else:
    print('Select 1, 2, or 3')
    sys.exit()