# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #ALARM HERE
        self.room_name = "1"
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('hello there!')

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('bye bye')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
# class ChatConsumer(WebsocketConsumer):

#     def connect(self):
#         print('hello there!')
#         self.accept()


#     # Receive message from WebSocket
#     def receive(self, text_data):
#         print('okey')
        # text_data_json = json.loads(text_data)
        # print(text_data_json)
        # command = text_data_json['command']
        # if(command == 'pre_load'):
        #     print('lol')
        #     #self.preLoadchats()
        # if(command == 'new_message'):
        #     self.new_message(text_data_json)
        # if(command == 'close'):
        #     self.load_close_data(text_data_json['last_read'])
        # if(command == 'complain'):
        #     self.complain(text_data_json)
        # if(command == 'delete_message'):
        #     self.delete_message(text_data_json)
        # if(command == 'edit_message'):
        #     self.edit_message(text_data_json)

    # def disconnect(self, close_code):
    #     print('finito')
        # if self.user.is_renter == True:
        #     for landlord in self.user.clients.all():
        #         chat = landlord.chat
        #         room_group_name = "chat_" + str(chat.pk)
        #         async_to_sync(self.channel_layer.group_add)(
        #             room_group_name,
        #             self.channel_name
        #         )
        #raise StopConsumer()


#        self.user_pk = self.scope['url_route']['kwargs']['user_pk']
#        self.user = CustomUser.objects.get(pk = self.user_pk)
#        self.moderators = set()
#/home/oleg/RAtest/RAsite/text.txt

#        #suppose
#        if self.user.is_renter:
#            for landlord in self.user.clients.all():
#                chat = landlord.chat
#                room_group_name = "chat_" + str(chat.pk)
#                async_to_sync(self.channel_layer.group_add)(
#                    room_group_name,
#                    self.channel_name
#                )
#                if self.user.is_moderator == False:
#                    self.moderators.add(chat.moderator_pk)
#
#        if self.user.is_moderator == True:
#            room_group_name = "moderator_" + str(self.user_pk)
#            async_to_sync(self.channel_layer.group_add)(
#                    room_group_name,
#                    self.channel_name
#                )
#        else:
#            for moderator_pk in self.moderators:
#                #на всякий случай, вообще такого не должно быть
#                if moderator_pk != -1:
#                    room_group_name = "moderator_" + str(moderator_pk)
#                    #print(room_group_name)
#                    async_to_sync(self.channel_layer.group_add)(
#                        room_group_name,
#                        self.channel_name
#                    )
#
#        if self.user.is_landlord:
#            chat = self.user.chat
#            room_group_name = "chat_" + str(chat.pk)
#            async_to_sync(self.channel_layer.group_add)(
#                room_group_name,
#                self.channel_name
#            )

#    def preLoadchats(self):
#        chats_list = []
#        if self.user.is_renter:
#            if self.user.is_moderator:
#                json_chat = self.chat_to_json(self.user.chat)
#                json_chat['is_moderator'] = 'yes'
#                chats_list.append(json_chat)
#            for landlord in self.user.clients.all():
#                chat = landlord.chat
#                chats_list.append(self.chat_to_json(chat))
#
#        # if self.user.is_landlord:
#        #     chat = self.user.chat
#        #     chats_list.append(self.chat_to_json(chat))
#
#        content = {
#                'command': 'preload_chats',
#                'chats': chats_list,
#            }
#        #print(content)
#        self.send_message(content)
#
#    def chat_to_json(self, chat):
#        chat_size = len(chat.users.all())
#        last_read_pk = LastReadMessage.objects.get(chat_pk = chat.pk, user_pk = self.user_pk).message_pk
#        #print(chat.pk, " ", self.user_pk)
#        return {
#            'name' : chat.name,
#            'pk' : chat.pk,
#            'size' : chat_size,
#            'last_read_pk' : last_read_pk,
#            'messages' : self.messages_to_json(chat.messages.order_by('-timestamp').all()),
#            'is_moderator' : 'no',
#        }
#
#    def messages_to_json(self, messages):
#        result = []
#        for message in messages:
#            result.append(self.message_to_json(message))
#        return result
#
#    def message_to_json(self, message):
#        return {
#            'author_name': message.author_name,
#            'author_pk': message.author.pk,
#            'content': message.content,
#            'time': message.getTime(),
#            'message_pk': message.pk,
#            'chat_pk': message.chat_pk,
#        }
#
#    def new_message(self, data):
#        text_message = data['content']
#        chat_pk = data['chat_pk']
#        chat = Chat.objects.get(pk = chat_pk)
#        message = Message.objects.create(
#                 author = self.user,
#                 author_name = self.user.name,
#                 content = text_message,
#                 chat_pk = chat_pk)
#        #chat.messages.add(message)
#        content = {
#              'command': 'new_message',
#              'message': self.message_to_json(message),
#              'chat_pk': chat_pk,
#        }
#        return self.send_chat_message(content)
#
#    def delete_message(self, data):
#        primary_key = data['pk']
#        msg = Message.objects.get(pk = primary_key)
#        msg.delete()
#        content = {
#              'command': 'delete_message',
#              'pk': primary_key,
#        }
#        return self.delete_chat_message(content)
#
#    def edit_message(self, data):
#        primary_key = data['pk']
#        msg = Message.objects.get(pk = primary_key)
#        if(msg.content != data['message']):
#            msg.content = data['message']
#            msg.save()
#            return self.edit_chat_message(data)
#
#    def load_close_data(self, data):
#        last_read = json.loads(data)
#        print(last_read)
#        for pair in last_read:
#            msg = LastReadMessage.objects.get(chat_pk = pair[0], user_pk = self.user_pk)
#            msg.message_pk = pair[1]
#            msg.save()
#
#    def complain(self, data):
#        message_pk = data['message_pk']
#        chat_pk  = data['chat_pk']
#        message = Message.objects.get(pk = message_pk)
#        chat = Chat.objects.get(pk = chat_pk)
#        moderator_pk = chat.moderator_pk
#        moderator = CustomUser.objects.get(pk = moderator_pk)
#        moderator_chat = moderator.chat
#
#        if len(moderator_chat.messages.filter(pk = message.pk)) == 0:
#            #do something in DB
#            moderator_chat.messages.add(message)
#            content = {
#                'command' : 'complain',
#                'moderator_pk' : moderator_pk,
#                'message' : self.message_to_json(message),
#                'moderator_chat_pk' : moderator_chat.pk,
#            }
#            self.send_chat_complain(content)
#        else:
#            print('kek')

#    # Receive message from room group
#    def chat_message(self, event):
#        message = event['message']
#        # Send message to WebSocket
#        self.send(text_data=json.dumps(message))
#
#    # Send message to room group
#    def send_chat_message(self, content):
#            room_group_name = "chat_" + str(content['chat_pk'])
#            async_to_sync(self.channel_layer.group_send)(
#            room_group_name,
#            {
#                'type': 'chat_message',
#                'message': content
#            })
#
#    def send_chat_complain(self, content):
#        room_group_name = "moderator_" + str(content['moderator_pk'])
#        async_to_sync(self.channel_layer.group_send)(
#        room_group_name,
#        {
#            'type': 'complain_message_local',
#            'message': content
#        })
#
#    def complain_message_local(self, event):
#        content = event['message']
#        #complaining message to WebSocket only for moderator
#        if ( int(self.user_pk) == int(content['moderator_pk'])):
#            self.send(text_data = json.dumps(content))
#
#    def send_message(self, content):
#        text_data = json.dumps(content)
#        self.send(text_data)


#     # commands = {
#     #     'pre_load' : pre_load_messages,
#     #     'new_message' : new_message,
#     #     'delete_message' : delete_message
#     # }

#     # # Send edited message to room group
#     # def edit_chat_message(self, content):
#     #         async_to_sync(self.channel_layer.group_send)(
#     #         self.room_group_name,
#     #         {
#     #             'type': 'edit_local_message',
#     #             'message': content
#     #         })

#     # Delete message from room group
#     def delete_chat_message(self, content):
#             async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'delete_local_message',
#                 'content': content
#             })

#     # Receive 'edited message' from room group
#     def edit_local_message(self, event):
#         content = event['message']
#         # 'Delete message' to WebSocket
#         self.send(text_data=json.dumps(content))

#     # Receive 'deleting message' from room group
#     def delete_local_message(self, event):
#         content = event['content']
#         # 'Delete message' to WebSocket
#         self.send(text_data=json.dumps(content))

# #python3 manage.py runserver
