from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import jwt
import json
from decouple import config
from rest_framework.response import Response
from .models import Messages,User
class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def getReciever(self,id):
        user=User.objects.get(pk=id)
        return user
    @database_sync_to_async
    def getUser(self,id):
        user=User.objects.get(pk=id)
        return user
    @database_sync_to_async
    def save_messages(self,message,sender,reciever,read):
        messages=Messages.objects.create(
            message=message,
            receipient=reciever,
            sender=sender,
            read=read
            )
        return messages
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, code):
        print (code)
    
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            sender_token = data.get('senderToken')
            recipient_id = data.get('recipientId')
            if data['chat'] is not None:
                message=data['chat']
            # print(message)
            mes='hello'
            # print(mes)
            if sender_token and recipient_id:
                SECRET_KEY = config('SECRET_KEY')
                # print(mes)
                try:
                    decoded_token = jwt.decode(sender_token, SECRET_KEY, algorithms=["HS256"])
                    self.sender_id = decoded_token.get('user_id')
                    self.sender_name = decoded_token.get('first_name')
                    print(self.sender_name)
                except jwt.DecodeError as e:
                    print(e)

                self.name = f'sender{self.sender_id}_recipient{recipient_id}'
                print(self.name)
                await self.channel_layer.group_add(self.name,self.channel_name)
                await self.channel_layer.group_send(
                self.name,
                {
                    'type': 'chat',
                    'message': mes,
                    'sender': self.sender_id,
                    'recipient':recipient_id
                },
            )
        except json.JSONDecodeError as e:
            print(e)
        
    async  def chat(self,event):
        print("chat method executed")
        try:
            print("Before extraction:", event)
            message =event.get('message')
            print(message)
            sender =  event.get('sender')
            recipient = event.get('recipient')
            recipientUser=await self.getReciever(recipient)
            userfunc=await self.getUser(sender)
            read='False'
            messageFunc=await self.save_messages(message,userfunc,recipientUser,read)
            print("After extraction:", message, sender, recipient)
            print(messageFunc)
            await self.send(json.dumps(messageFunc))
            # Further processing or sending the message to the client can be added here
        except Exception as e:
            print (str(e))