import socket
import os
import struct
import log
from interfaces.api.server_app import complete

SOCKET_PATH = "/tmp/local_app.sock"


def start_socket_server():
    while True:
        _listen_on_socket()


def _listen_on_socket():
    try:
        os.unlink(SOCKET_PATH)
    except FileNotFoundError:
        pass

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(SOCKET_PATH)
        server.listen(1)

        conn, _ = server.accept()

        try:
            while True:
                size = struct.unpack("I", _recv_exact(conn, 4))[0]
                if size == 0:
                    return

                data = _recv_exact(conn, size)

                try:
                    data_string = data.decode("utf-8")
                    _handle_message(data_string)
                except UnicodeDecodeError as e:
                    print("Received non-UTF-8 data: ", e)
        except Exception as e:
            print("Error while receiving data: ", e)
            return


# Source - https://stackoverflow.com/a/61976453
# Posted by tdelaney
# Retrieved 2026-07-27, License - CC BY-SA 4.0


def _recv_exact(sockobj, size) -> bytes:
    buflist = []
    while size:
        buf = sockobj.recv(size)
        if not buf:
            raise EOFError("Socket closed with %d bytes left in this recv" % size)

        buflist.append(buf)
        size -= len(buf)
    return b"".join(buflist)


def _handle_message(message: str):
    log.log("Received message: " + message)

    complete(message)
