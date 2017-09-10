#!/usr/bin/env python3

import sys
import math
import base64
import tkinter
import subprocess
from io import BytesIO
from PIL import Image as PILImage
from websocket_server import WebsocketServer
import string

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
	print("Client(%d) said: %s" % (client['id'], message))

	if "/9j" in message:
		image = open('test.jpg', 'wb')
		image.write(base64.decodestring(str.encode(message)))

		p = subprocess.Popen(["python3", "../app/script.py"], stdout=subprocess.PIPE)
		print(p.communicate())


PORT=9001
HOST="10.196.44.64"
server = WebsocketServer(PORT, HOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
