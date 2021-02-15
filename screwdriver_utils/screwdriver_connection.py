import logging
import os
import socket
import sys
import time
import numpy as np


_log = logging.getLogger("Screwdriver")


class Screwdriver:

    def __init__(self, ip_addr="192.168.1.1"):
        self.ip_addr = ip_addr
        port = 502 #51234 #49151
        self.ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.ctrl_socket.connect((self.ip_addr, port))
            _log.info("Successfully connected to Screwdriver!\n")
        except Exception as e: 
            print("something's wrong with %s:%d. Exception is %s" % (self.ip_addr, port, e))
        
        self.buff_size = 1024


    def __del__(self):
        _log.info("Closing socket\n")
        self.ctrl_socket.shutdown(socket.SHUT_RDWR)
        self.ctrl_socket.close()


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


    def sd_move(self, shank_pos_mm):
        program = "sd_move("+str(shank_pos_mm)+",0)\n"
        self._send_ascii_bytes(program, self.ctrl_socket)


    def get_sd_Busy(self):
        program = "get_sd_Busy()\n"
        self._send_ascii_bytes(program, self.ctrl_socket)
        #time.sleep(0.12)  # seconds
        reply = self._receive_ascii_bytes(self.ctrl_socket)
        return reply