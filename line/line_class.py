import requests
import json
from datetime import datetime

from django.conf import settings

from accounts import models
from history.models import ReservartionHistory

class Line():

    def __init__(self, body, *args, **kwargs):
        self.channel_secret = settings.CHANNEL_SECRET
        self.channel_access_token = settings.CHANNEL_ACCESS_TOKEN
        self.json_body = json.loads(body)

    def receive_message(self):
        message_type = self.json_body['events'][0]['type']
        user_id = self.json_body['events'][0]['source']['userId']
        timestamp = self.json_body['events'][0]['timestamp']
        reply_token = self.json_body['events'][0]['replyToken']
        user, user_meta_data = self.get_user_info_line(user_id=user_id)
        if message_type == 'message':
            message = self.json_body['events'][0]['message'].get('text', None)
            if message:
                if message == 'create':
                    ReservartionHistory.objects.create(user=user.id, user_name=user.username)
                    meta_data = self.location_action(reply_token)
                elif message == 'cancle':
                    self.handle_cancle(user_id=user.id)
                    meta_data = self.initial_action(reply_token)
                else:
                    # meta_data = self.send_summary(user_id=user.id,reply_token=reply_token)
                    meta_data = self.initial_action(reply_token)
            else:  # ส่ง location กลับมา
                self.handle_location_message(user_id=user.id, reply_token=reply_token)
                meta_data = self.date_picker_action(reply_token=reply_token)

        elif message_type == 'location':
            self.handle_location_message(meta_data)
            self.date_picker_action(reply_token)
            
        elif message_type == 'postback':  # ส่ง date กลับมา
            self.handle_datepicker(user.id)
            meta_data = self.send_summary(user_id=user.id, meta_data=user_meta_data, reply_token=reply_token)

        self.reply_message(meta_data)
        return
    
    def send_summary(self, user_id, reply_token, meta_data):
        reserve = ReservartionHistory.objects.filter(user=user_id, is_cancled=False).order_by('-pk').first()
        json_location = json.loads(reserve.location)
        reserved_data = datetime.strftime(reserve.reserved_date, '%d/%m/%Y %H:%M')
        address = json_location['address']
        displayName = meta_data['displayName']
        userId = meta_data['userId']
        data = {
            'replyToken': reply_token,
            'messages': [
                {
                    'type': 'text',
                    'text': f'คุณ {displayName} ได้ทำการจอง\n ที่ {address}\n เวลา {reserved_data}'
                }
            ]
        }
        return data
        
    def handle_datepicker(self, user_id):
        lastest_reserve = ReservartionHistory.objects.filter(user=user_id, is_cancled=False).order_by('-pk').first()
        postback_time = self.json_body['events'][0]['postback']['params']['datetime']
        lastest_reserve.reserved_date = datetime.strptime(postback_time, '%Y-%m-%dT%H:%S')
        lastest_reserve.save(update_fields=['reserved_date'])
        return

    def handle_text_message(self, meta, reply_token):
        self.reply_message('success', reply_token)

    def handle_cancle(self, user_id):
        lastest_reserve = ReservartionHistory.objects.filter(user=user_id, is_cancled=False).order_by('-pk').first()
        lastest_reserve.is_cancled = True
        lastest_reserve.save(update_fields=['is_cancled'])

    def handle_location_message(self, user_id, reply_token):
        lastest_reserve = ReservartionHistory.objects.filter(user=user_id, is_cancled=False).order_by('-pk').first()
        location_data = self.json_body['events'][0]['message']
        lastest_reserve.location = json.dumps(location_data)
        lastest_reserve.save(update_fields=['location'])
        meta_data = self.location_action(reply_token)
        return meta_data

    def http_request(self, method=None, data=None, url=None):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.CHANNEL_ACCESS_TOKEN}'
        }
        try:
            response = requests.request(method=method, data=data, url=url, headers=headers)
            if response.status_code >= 200 or response.status_code <= 300:
                return response.json()
            else:
                return False
        except Exception as error:
            print('error', error)
            return False

    def reply_message(self, meta_data):
        url = 'https://api.line.me/v2/bot/message/reply'
        response = self.http_request(method='POST', data=json.dumps(meta_data), url=url)

    def location_action(self, reply_token):
        data = {
            'replyToken': reply_token,
            "messages": [{
                "type": "text",
                "text": "กรุณาเลือกสถานที่",
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type":"location",
                                "label":"กดเพื่อเลือกสถานที่"
                            }  
                        },
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"ยกเลิก",
                                "text": "cancle"
                            }
                        },
                    ]
                }
            }]
        }
        return data
    
    def initial_action(self, reply_token):
        data = {
            'replyToken': reply_token,
            "messages": [{
                "type": "text",
                "text": "กรุณาเลือกข้อความ",
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"เริ่มจอง",
                                "text": "create"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"ยกเลิก",
                                "text": "cancle"
                            }
                        },
                    ]
                }
            }]
        }
        return data

    def message_action(self, reply_token):
        data = {
            'replyToken': reply_token,
            "messages": [{
                "type": "text",
                "text": "กรุณาเลือกข้อความ",
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"เลือกว้นที่",
                                "text": "datepicker"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"เลือกสถานที่",
                                "text": "location"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"ยกเลิก",
                                "text": "cancle"
                            }
                        },
                    ]
                }
            }]
        }
        return data

    def date_picker_action(self, reply_token):
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.CHANNEL_ACCESS_TOKEN}'
        }
        data = {
            'replyToken': reply_token,
            "messages": [{
                "type": "text",
                "text": "กดเพื่อเลือกวันที่และเวลา",
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type":"datetimepicker",
                                "label":"กดเลือกวันที่และเวลา",
                                "data":"storeId=12345",
                                "mode":"datetime",
                                "initial":"2017-12-25t00:00",
                                "max":"2018-01-24t23:59",
                                "min":"2017-12-25t00:00"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type":"message",
                                "label":"ยกเลิก",
                                "text": "cancle"
                            }
                        },
                    ]
                }
            }]
        }
        return data
    
    def get_user_info_line(self, user_id):
        url = 'https://api.line.me/v2/bot/profile/' + user_id
        response = self.http_request(method='GET', url=url)
        line_id = response['userId']
        username = response['displayName']
        if response:
            user, created = models.User.objects.get_or_create(
                line = line_id,
                username = username,
            )
            return  user, response
