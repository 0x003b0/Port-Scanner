import colorama
import validators

#PURPOSE: Handle IP Address or Domain target inserted by user
def get_IP_target():
    while True:
        target = input(colorama.Fore.CYAN + "[IP / DOMAIN TARGET]: " + colorama.Style.RESET_ALL).strip() #strip() rimuove spazi prima e dopo l'input
        if target:
            if validators.is_valid_ip(target) or validators.is_valid_domain(target):
                return target
            else:
                print(colorama.Fore.RED + "[ERROR] Invalid IP Address or domain name.\n")
                continue
        print(colorama.Fore.RED + "[ERROR] IP Address value cannot be empty.\n")

#PURPOSE: Handle Port target inserted by user
def get_port_target():
    while True:
        try:
           port = int(input(colorama.Fore.CYAN + "[PORT TARGET]: " + colorama.Style.RESET_ALL))
           if validators.is_valid_port(int(port)):
               return port
           else:
               print(colorama.Fore.RED + "[ERROR] Invalid port. Please enter a number between 1 and 65535.\n")
        except ValueError:
            print(colorama.Fore.RED + "[ERROR] Invalid format. Use <port> (e.g. 80).\n")

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

            if validators.is_valid_range(first_port, last_port):
                return first_port, last_port
            else:
                print(colorama.Fore.RED + "[ERROR] Invalid port range. Valid ports must be between 1 and 65535.\n")

        except (ValueError, IndexError):
            print(colorama.Fore.RED + "[ERROR] Invalid format. Use: <start>-<end> (e.g. 40-100).\n")

#PURPOSE: Ask user for multiple Ports separated by comma/s
def get_ports_target_separated_by_commas():
    while True:
        user_ports_comma_input = input(colorama.Fore.CYAN + "[PORTS TARGETS] (e.g.: 80,110,443): " + colorama.Style.RESET_ALL).strip()

        try:
            user_ports_comma = [n.strip() for n in user_ports_comma_input.split(",")] #rimuove le virgole e spazi creando una lista con n elementi chiamata user_ports_comma

            if len(user_ports_comma) == 1:
                raise ValueError
            
            if all(validators.is_valid_port(int(n)) for n in user_ports_comma):
                return user_ports_comma
            else:
                print(colorama.Fore.RED + "[ERROR] Invalid port/s value/s. Valid ports must be between 1 and 65535.\n")  

        except (ValueError, IndexError):
            print(colorama.Fore.RED + "[ERROR] Invalid format. Use: <port1>,<port2>,... (e.g. 80,110).\n")