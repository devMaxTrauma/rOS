try:
    import bluetooth
except ImportError:
    raise ImportError("Bluetooth not found or failed to load.")
try:
    import threading
except ImportError:
    raise ImportError("Threading not found or failed to load.")
try:
    import time
except ImportError:
    raise ImportError("Time not found or failed to load.")

client_info = None
client_sock = None
bluetooth_rx_thread = None
bluetooth_connected = False
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
connected_callback = None
recv_callback = None


port = server_sock.getsockname()[1]
uuid = "00001101-0000-1000-8000-00805F9B34FB"
service_name = "FindMy"

bluetooth_connect_try_enabled = True


def try_routine():
    global bluetooth_connected
    if bluetooth_connected:
        time.sleep(1)
        return

    global client_info
    global client_sock
    global bluetooth_rx_thread

    try:
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)
        bluetooth_connected = True
        bluetooth_rx_thread = threading.Thread(target=bluetooth_rx_interrupt).start()
        if connected_callback is not None: connected_callback()
    except Exception as e:
        bluetooth_connected = False
        if client_sock is not None: client_sock.close()
        if bluetooth_rx_thread is not None: bluetooth_rx_thread.join()
        bluetooth_rx_thread = None
        print("RBluetooth: Error: Error in bluetooth connection.")
        print(e)
        print("RBluetooth: retrying...")
        pass
    pass


def bluetooth_connect_try():
    global bluetooth_connected
    global client_sock
    global client_info
    global bluetooth_rx_thread

    while bluetooth_connect_try_enabled: try_routine()


def recv():
    while bluetooth_connected:
        data = client_sock.recv(1024)
        if not data: break
        print("Received: " + str(data))
        if recv_callback is None: continue
        recv_callback(data)


def bluetooth_rx_interrupt():
    global bluetooth_connected
    global client_sock
    global recv_callback
    try:
        recv()
    except Exception as e:
        print("Error in rx_interrupt.")
        print(e)
        bluetooth_connected = False
        pass


def close():
    global bluetooth_rx_thread
    global try_thread
    global client_sock
    global server_sock
    global recv_callback

    global bluetooth_connect_try_enabled
    bluetooth_connect_try_enabled = False
    global bluetooth_connected
    bluetooth_connected = False

    recv_callback = None
    print("Bluetooth closed.")


try:
    bluetooth.advertise_service(server_sock, service_name,
                                service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])
except Exception as e:
    print("Error in bluetooth advertise_service.")

try_thread = threading.Thread(target=bluetooth_connect_try).start()
print("now you can connect to the bluetooth.")
