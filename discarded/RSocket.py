# this code is for socket transfer
import socket
import threading


def __init__(self, ip, port):
    print("Socket connecting to " + ip + ":" + str(port) + "...")
    self.ip = ip
    self.port = port
    self.socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
    print("Socket created.")
    self.socket.bind((self.ip, self.port))
    print("Socket connected to " + self.ip + ":" + str(self.port) + ".")
    self.socket.listen(1)
    rkey = RKey()
    self.socket.settimeout(rkey.get_key("SLDConnectTimeout").get("value"))
    print("Socket listening...")

    while True:
        try:
            print("looped fuck")
            self.sld_socket, self.sld_address = self.socket.accept()
            print("Connected to " + str(self.sld_address) + ".")
            self.sld_rx_thread = self.threading.Thread(target=self.socket_rx_thread, args=(self.sld_socket,))
            self.sld_rx_thread.start()
            if self.sld_socket:
                break
        except socket.timeout:
            print("timeout")
            break


def socket_rx_thread(self, sld_socket):
    try:
        while True:
            data = sld_socket.recv(1024)
            if not data:  # if data is empty
                continue
            elif data == b"exit":  # if data is "exit"
                break
            print("Received: " + str(data))
    except Exception as e:
        print("Error in socket_rx_thread.")
        print(e)
    finally:
        sld_socket.close()
        print("Socket closed.")


def send(self, data):
    self.socket.send(data)


def receive(self):
    return self.socket.recv(1024)


def close(self):
    self.sld_rx_thread.join()
    self.socket.close()
    print("Socket closed.")
