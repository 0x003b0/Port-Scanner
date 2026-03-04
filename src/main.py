import colorama
import pyfiglet
import sys
import scanner
import input_handlers

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

#PURPOSE: Handle the user choose
def handle_user_choice(user_choose):
    if user_choose == 1:
        ip = input_handlers.get_IP_target()
        port = input_handlers.get_port_target()
        scanner.scan_port(ip, port)
    elif user_choose == 2:
        ip = input_handlers.get_IP_target()
        first_port, last_port = input_handlers.get_port_range_target()
        scanner.scan_ports(ip, first_port, last_port)
    elif user_choose == 3:
        print('Exiting...')
        sys.exit()
    else:
        print(colorama.Fore.RED + "[ERROR] Select option 1, 2 or 3.\n")
        sys.exit()

#PURPOSE: Ask user for a menu option
def get_menu_user_choice():
    try:
        user_choice = int(input(colorama.Fore.CYAN + "[>]: " + colorama.Style.RESET_ALL))
        handle_user_choice(user_choice)
    except ValueError:
        print(colorama.Fore.RED + "[ERROR] Invalid format. Use: <option>.\n")

program_title()
show_menu()
get_menu_user_choice()