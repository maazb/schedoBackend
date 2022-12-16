
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import datetime
import firebase_admin

from firebase_admin import messaging
from firebase_admin import credentials
def initializeFB():
    cred = credentials.Certificate("schedomeet-firebase.json")
    firebase_admin.initialize_app(credential= cred , options=None, name='[DEFAULT]')

def send_to_token():
    # [START send_to_token]
    # This registration token comes from the client FCM SDKs.
    registration_token = 'YOUR_REGISTRATION_TOKEN'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_token]


def send_to_topic():
    # [START send_to_topic]
    # The topic name can be optionally prefixed with "/topics/".
    topic = 'highScores'

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_topic]


def send_to_condition():
    # [START send_to_condition]
    # Define a condition which will send to devices which are subscribed
    # to either the Google stock or the tech industry topics.
    condition = "'stock-GOOG' in topics || 'industry-tech' in topics"

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        condition=condition,
    )

    # Send a message to devices subscribed to the combination of topics
    # specified by the provided condition.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # [END send_to_condition]


def send_dry_run():
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token='token',
    )

    # [START send_dry_run]
    # Send a message in the dry run mode.
    response = messaging.send(message, dry_run=True)
    # Response is a message ID string.
    print('Dry run successful:', response)
    # [END send_dry_run]


def android_message():
    # [START android_message]
    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                title='$GOOG up 1.43% on the day',
                body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                icon='stock_ticker_update',
                color='#f45342'
            ),
        ),
        topic='industry-tech',
    )
    # [END android_message]
    return message


def apns_message():
    # [START apns_message]
    message = messaging.Message(
        apns=messaging.APNSConfig(
            headers={'apns-priority': '10'},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title='$GOOG up 1.43% on the day',
                        body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                    ),
                    badge=42,
                ),
            ),
        ),
        topic='industry-tech',
    )
    # [END apns_message]
    return message


def webpush_message():
    # [START webpush_message]
    message = messaging.Message(
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title='$GOOG up 1.43% on the day',
                body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
                icon='https://my-server/icon.png',
            ),
        ),
        topic='industry-tech',
    )
    # [END webpush_message]
    return message


def all_platforms_message():
    # [START multi_platforms_message]
    message = messaging.Message(
        notification=messaging.Notification(
            title='$GOOG up 1.43% on the day',
            body='$GOOG gained 11.80 points to close at 835.67, up 1.43% on the day.',
        ),
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                icon='stock_ticker_update',
                color='#f45342'
            ),
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(badge=42),
            ),
        ),
        topic='industry-tech',
    )
    # [END multi_platforms_message]
    return message


def subscribe_to_topic():
    topic = 'highScores'
    # [START subscribe]
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_n',
    ]

    # Subscribe the devices corresponding to the registration tokens to the
    # topic.
    response = messaging.subscribe_to_topic(registration_tokens, topic)
    # See the TopicManagementResponse reference documentation
    # for the contents of response.
    print(response.success_count, 'tokens were subscribed successfully')
    # [END subscribe]


def unsubscribe_from_topic():
    topic = 'highScores'
    # [START unsubscribe]
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_n',
    ]

    # Unubscribe the devices corresponding to the registration tokens from the
    # topic.
    response = messaging.unsubscribe_from_topic(registration_tokens, topic)
    # See the TopicManagementResponse reference documentation
    # for the contents of response.
    print(response.success_count, 'tokens were unsubscribed successfully')
    # [END unsubscribe]


def new_meeting( tokens: list[str], title: str, date: str):
    # cred = credentials.Certificate("schedomeet-firebase.json")
    # firebase_admin.initialize_app(credential= cred , options=None, name='[DEFAULT]')
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    date_str =date_object. strftime("%A,%d %B")
    # [START send_all]
    # Create a list containing up to 500 messages.
    messages = []
    
    print( len(tokens))
    for x in tokens:
        print(x)
        if(x != ""):
            messages.append(messaging.Message(
                notification=messaging.Notification('New meeting', 'New meeting arranged "' + title + '"' + ' on ' + date_str),
                token=x,
            ),)
            
    response = messaging.send_all(messages)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))
    
    
def new_event( tokens: list[str], title: str, date: str):
    # cred = credentials.Certificate("schedomeet-firebase.json")
    # firebase_admin.initialize_app(credential= cred , options=None, name='[DEFAULT]')
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    date_str =date_object. strftime("%A,%d %B")
    # [START send_all]
    # Create a list containing up to 500 messages.
    messages = []
    
    print( len(tokens))
    for x in tokens:
        print(x)
        if(x != ""):
            messages.append(messaging.Message(
                notification=messaging.Notification('New event', 'New event arranged "' + title + '"' + ' on ' + date_str),
                token=x,
            ),)
            
    response = messaging.send_all(messages)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))


def meeting_cancelled( tokens: list[str], meeting):
    # cred = credentials.Certificate("schedomeet-firebase.json")
    # firebase_admin.initialize_app(credential= cred , options=None, name='[DEFAULT]')
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    # date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    # date_str =date_object. strftime("%A,%d %B")
    # [START send_all]
    # Create a list containing up to 500 messages.
    messages = []
    title = meeting.title
    
    print( len(tokens))
    for x in tokens:
        print(x)
        if(x != ""):
            messages.append(messaging.Message(
                notification=messaging.Notification('Meeting cancelled', 'Meeting "' + title + '"' + ' has been cancelled.'),
                token=x,
            ),)
            
    response = messaging.send_all(messages)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))
    
def event_cancelled( tokens: list[str], event):
    
    registration_token = 'YOUR_REGISTRATION_TOKEN'
    # date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    # date_str =date_object. strftime("%A,%d %B")
    # [START send_all]
    # Create a list containing up to 500 messages.
    messages = []
    title = event.title
    
    print( len(tokens))
    for x in tokens:
        print(x)
        if(x != ""):
            messages.append(messaging.Message(
                notification=messaging.Notification('Event cancelled', 'Event "' + title + '"' + ' has been cancelled.'),
                token=x,
            ),)
            
    response = messaging.send_all(messages)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))

def send_multicast():
    # [START send_multicast]
    # Create a list containing up to 500 registration tokens.
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_N',
    ]

    message = messaging.MulticastMessage(
        data={'score': '850', 'time': '2:45'},
        tokens=registration_tokens,
    )
    response = messaging.send_multicast(message)
    # See the BatchResponse reference documentation
    # for the contents of response.
    print('{0} messages were sent successfully'.format(response.success_count))
    # [END send_multicast]


def send_multicast_and_handle_errors():
    # [START send_multicast_error]
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        'YOUR_REGISTRATION_TOKEN_1',
        # ...
        'YOUR_REGISTRATION_TOKEN_N',
    ]

    message = messaging.MulticastMessage(
        data={'score': '850', 'time': '2:45'},
        tokens=registration_tokens,
    )
    response = messaging.send_multicast(message)
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(registration_tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))
    # [END send_multicast_error]
