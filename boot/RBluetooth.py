def __init__(self):
    self.sound_engine = RSound()
    self.client_info = None
    self.client_sock = None
    self.bluetooth_rx_thread = None
    self.bluetooth_connected = False
    self.bluetooth = __import__("bluetooth")
    self.threading = __import__("threading")
    self.server_sock = self.bluetooth.BluetoothSocket(self.bluetooth.RFCOMM)
    self.server_sock.bind(("", self.bluetooth.PORT_ANY))
    self.server_sock.listen(1)

    self.port = self.server_sock.getsockname()[1]
    self.uuid = "00001101-0000-1000-8000-00805F9B34FB"
    self.service_name = "FindMy"

    try:
        self.bluetooth.advertise_service(self.server_sock, self.service_name,
                                         service_id=self.uuid,
                                         service_classes=[self.uuid, self.bluetooth.SERIAL_PORT_CLASS],
                                         profiles=[self.bluetooth.SERIAL_PORT_PROFILE])
    except Exception as e:
        print("Error in bluetooth advertise_service.")

    self.try_thread = self.threading.Thread(target=self.bluetooth_connect_try).start()
    print("now you can connect to the bluetooth.")


def bluetooth_connect_try(self):
    while True:
        try:
            if self.bluetooth_connected:
                import time
                time.sleep(1)
                continue
            self.server_sock.settimeout(10)
            self.client_sock, self.client_info = self.server_sock.accept()
            print("Accepted connection from", self.client_info)
            self.bluetooth_rx_thread = self.threading.Thread(target=self.bluetooth_rx_interrupt,
                                                             args=(self.client_sock,)).start()

            if self.client_sock:
                print("connected.")
                self.bluetooth_connected = True
                # break
            pass
        except Exception as e:
            if self.bluetooth_rx_thread is not None:
                self.client_sock.close()
                self.bluetooth_rx_thread.join()
                self.bluetooth_rx_thread = None
                pass
            print("RBluetooth: Error: Error in bluetooth connection.")
            print(e)
            print("RBluetooth: retrying...")
            pass
        pass


def bluetooth_rx_interrupt(self, client_sock):
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received: " + str(data))

            if data == b"a":
                self.sound_engine.play("FindMy.mp3")
                pass
    except Exception as e:
        print("Error in rx_interrupt.")
        print(e)
        self.bluetooth_connected = False
        pass


def close(self):
    self.sound_engine.pygame.quit()
    if self.bluetooth_rx_thread is not None:
        self.client_sock.close()
        self.bluetooth_rx_thread.join()
        self.bluetooth_rx_thread = None
        pass
    if self.try_thread is not None:
        self.try_thread.join()
    self.server_sock.close()
    print("Bluetooth closed.")
