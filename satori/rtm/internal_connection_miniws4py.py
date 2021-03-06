
from miniws4py.client import WebSocketBaseClient

import satori.rtm.internal_logger


class RtmWsClient(WebSocketBaseClient):

    def __init__(self, *args, **kwargs):
        WebSocketBaseClient.__init__(self, *args, **kwargs)
        self.logger = satori.rtm.internal_logger.logger
        self.delegate = None

    def send_ping(self):
        self.ping('py')

    def opened(self):
        if self.delegate:
            self.delegate.on_ws_opened()

    def ponged(self, _pong):
        if self.delegate:
            self.delegate.on_ws_ponged()

    def close(self, code=1000, reason=''):
        if self.terminated:
            raise RuntimeError('Connection is already closed')
        WebSocketBaseClient.close(self, code, reason)

    def closed(self, code, reason=None):
        if reason != 'Going away' and code != 1000:
            self.logger.error('Websocket closed because %s', reason)
        if self.delegate:
            self.delegate.on_ws_closed()

    def received_message(self, message):
        d = message.data
        if self.delegate:
            if self.protocols == ['cbor']:
                assert message.is_binary
                self.delegate.on_incoming_binary_frame(d)
            else:
                assert message.is_text
                self.delegate.on_incoming_text_frame(d.decode('utf8'))
