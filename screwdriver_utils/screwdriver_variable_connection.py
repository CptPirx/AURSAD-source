import logging
import os
import socket
import sys
import threading
import time
from queue import Queue

import numpy as np

_log = logging.getLogger("ScrewdriverVariableConnection")


class ScrewdriverVariableConnection:
    # ip_adr: <string>
    # controller_socket, dashboard_socket: <socket>
    # is_logging_data: <bool>

    def __init__(self, 
                ip_adr,
                controller_port=30002,
                controller_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.ip_adr = ip_adr
        self.port = controller_port

        self.controller_socket = None
        self.__output_config = None
        self.__input_config = {}
        self.__skipped_package_count = 0

        
        self.connect()

    def connect(self):
        if self.controller_socket:
            return

        self.__buf = b'' # buffer data in binary format
        try:
            self.controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.controller_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.controller_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.__skipped_package_count = 0
            self.controller_socket.connect((self.ip_adr, self.port))
        except (socket.timeout, socket.error):
            self.controller_socket = None
            raise


    def _receive_ascii_bytes(self, socket):
        reply = socket.recv(self.buff_size)
        _log.info(f"receiving bytes:{reply}")
        reply_ascii = reply.decode(encoding="ascii")
        _log.info(f"receiving:{reply_ascii}")
        return reply_ascii

    def _send_ascii_bytes(self, msg, socket):
        to_send = bytes(msg, encoding="ASCII")
        _log.info(f"sending:{to_send}")
        socket.sendall(to_send)
        _log.info("sent.")

    def __del__(self):
        # Should it stop recording here???
        # TODO : When deleting the object, make sure that only connected sockets will be closed.
        self.controller_socket.shutdown(socket.SHUT_RDWR)
        self.controller_socket.close()

    # def _ensure_ready(self):
    #     reply = "Program running: true"
    #     while not reply.startswith("Program running: false"):
    #         time.sleep(0.12)  # seconds
    #         self._send_ascii_bytes("running\n", self.dashboard_socket)
    #         reply = self._receive_ascii_bytes(self.dashboard_socket)
    #     assert reply.startswith("Program running: false"), reply

    def _send_ctrl_cmd(self, program):
        self._send_ascii_bytes(program, self.controller_socket)
        #self._ensure_ready()


