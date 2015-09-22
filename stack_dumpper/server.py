from collections import namedtuple
import os
from socketserver import BaseRequestHandler, ThreadingUnixStreamServer
from threading import Thread
import struct

from stack_dumpper.dumpper import call_once

server = None
server_thread = None

Protocol = namedtuple('Protocol', ('identifier', 'struct'))


class StackDumpperProtocolhandler(BaseRequestHandler):
    protocol = {
        'request': Protocol(1 << 0, '!L'),
        'response': Protocol(1 << 1, '!L'),
        'continue': Protocol(1 << 2, '!L')
    }

    def handle(self):
        data = self.request.recv(struct.calcsize(self.protocol['request'].struct))
        print(struct.unpack(self.protocol['request'].struct, data) == self.protocol['request'])


@call_once
def start_server():
    global server, server_thread
    socket_location = os.path.join('/tmp/dumpper-{}.socket'.format(os.getpid()))
    server = ThreadingUnixStreamServer((socket_location), StackDumpperProtocolhandler)
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print('Server started in', socket_location)


if __name__ == '__main__':
    start_server()
    server_thread.join()
