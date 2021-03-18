import json
from asgiref.sync import sync_to_async,async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChangllengeConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("challenge", self.channel_name)
        print("connected",self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("challenge", self.channel_name)
        self.close()

    def challenge_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))