
import socket
import argparse
import time
from datetime import datetime


# Authorized scanning targets only
ALLOWED_TARGETS = {"localhost", "127.0.0.1", "scanme.nmap.org"}

DEFAULT_PORTS = [21, 22, 80, 443]


def validate_ports(ports):
    """Validate that all ports are within the legal TCP port range."""
    if not ports:
        raise ValueError("At least one port must be specified.")

    for port in ports:
        if port < 1 or port > 65535:
            raise ValueError(f"Invalid port number: {port}")

    return sorted(set(ports))


def scan_port(target_ip, port, timeout):
    """Attempt a TCP connection to determine whether a port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))

            if result == 0:
                print(f"[OPEN]   Port {port}")
                return True
            else:
                print(f"[CLOSED] Port {port}")
                return False

    except socket.timeout:
        print(f"[TIMEOUT] Port {port}")
        return False

    except OSError as error:
        print(f"[ERROR] Port {port}: {error}")
        return False


def start_scan(target, ports, timeout, delay):
    """Resolve the target and scan the requested TCP ports."""

    if target.lower() not in ALLOWED_TARGETS:
        print("[ERROR] Unauthorized target.")
        print("[INFO] Only localhost and scanme.nmap.org are permitted.")
        return

    print("=" * 50)
    print("PYTHON TCP PORT SCANNER")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"Ports: {len(ports)}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # Resolve the hostname to an IPv4 address.
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Resolved IP: {target_ip}")

    except socket.gaierror:
        print("[ERROR] Unable to resolve hostname.")
        return

    open_count = 0
    start_time = time.time()

    # Scan each requested port with a delay between attempts.
    for port in ports:
        if scan_port(target_ip, port, timeout):
            open_count += 1

        time.sleep(delay)

    elapsed = time.time() - start_time

    print("-" * 50)
    print("SCAN SUMMARY")
    print(f"Total ports scanned: {len(ports)}")
    print(f"Open ports: {open_count}")
    print(f"Closed/Unresponsive ports: {len(ports) - open_count}")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="TCP Port Scanner - Authorized Targets Only"
    )

    parser.add_argument(
        "target",
        help="Target hostname or IP address"
    )

    port_group = parser.add_mutually_exclusive_group()

    port_group.add_argument(
        "--ports",
        help="Comma-separated ports (example: 22,80,443)"
    )

    port_group.add_argument(
        "--range",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        help="Port range (example: --range 1 100)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Connection timeout in seconds (default: 0.5)"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay between scans in seconds (default: 0.1)"
    )

    args = parser.parse_args()

    try:
        if args.timeout <= 0 or args.timeout > 10:
            raise ValueError("Timeout must be greater than 0 and at most 10 seconds.")

        if args.delay < 0 or args.delay > 10:
            raise ValueError("Delay must be between 0 and 10 seconds.")

        if args.ports:
            ports = [
                int(port.strip())
                for port in args.ports.split(",")
            ]

        elif args.range:
            start, end = args.range

            if start > end:
                raise ValueError("Starting port cannot exceed ending port.")

            ports = list(range(start, end + 1))

        else:
            ports = DEFAULT_PORTS

        ports = validate_ports(ports)

        start_scan(args.target, ports, args.timeout, args.delay)

    except ValueError as error:
        print(f"[INPUT ERROR] {error}")


if __name__ == "__main__":
    main()

