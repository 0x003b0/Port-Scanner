import socket
import colorama
import errno

#PURPOSE: Print Scanner Header results
def print_scanner_header():
    print("\nPORT     STATE       SERVICE         VERSION")
    print("─────    ────────    ───────         ─────────────────")

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