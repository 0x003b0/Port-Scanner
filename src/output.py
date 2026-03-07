import socket
import colorama
import errno
import services_dictionary
import banner_grabbing


#PURPOSE: Print Scanner Header results
def print_scanner_header():
    print("\nPORT     STATE       SERVICE         VERSION")
    print("─────    ────────    ───────         ───────────────────────────────")

#PURPOSE: Return/get Port Service
def get_port_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return services_dictionary.CUSTOM_SERVICES.get(port, "unknown")

#PURPOSE: Print results of a scan
def print_results(port, status_connection, s_socket):
    if status_connection == 0:
        status = "OPEN"
        service = get_port_service(port)
        banner = banner_grabbing.capture(port, s_socket)
        print(colorama.Fore.GREEN + f"{port:<9}{status:<12}{service:<16}{banner}" + colorama.Style.RESET_ALL)
    elif status_connection in (errno.ECONNREFUSED, 10061):
        status = "CLOSED"
        banner = "-"
        service = get_port_service(port)
        print(colorama.Fore.RED + f"{port:<9}{status:<12}{service:<16}{banner}" + colorama.Style.RESET_ALL)
    elif status_connection in (errno.ETIMEDOUT, errno.EHOSTUNREACH, 10060, 10035):
        status = "FILTERED"
        banner = "-"
        service = get_port_service(port)
        print(colorama.Fore.YELLOW + f"{port:<9}{status:<12}{service:<16}{banner}" + colorama.Style.RESET_ALL)
    else:
        status = f"ERROR (Codice: {status_connection})"
        print(status)