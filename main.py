import sys
import os
sys.path.append("vendor")
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import asyncio
import json
from src.providers.messages.messages import Messages
from src.neru import Neru
from src.providers.scheduler.contracts.startAtParams import StartAtParams
from src.providers.scheduler.scheduler import Scheduler
from src.providers.state.state import State
from src.providers.voice.voice import Voice
from src.providers.messages.contracts.messageContact import MessageContact
from src.providers.voice.contracts.vapiEventParams import VapiEventParams

app = Flask(__name__)
neru = Neru()


if os.getenv('NERU_CONFIGURATIONS') is None:
    print("NERU_CONFIGURATIONS environment variable is not set")
    sys.exit(1)

contact = json.loads(os.getenv('NERU_CONFIGURATIONS'))['contact']

async def listenForInboundCall():
    try:
        session = neru.createSession()
        voice = Voice(session)
        await voice.onVapiAnswer('onCall').execute()

        return 'OK'
    except Exception as e:
        print(e)
        return f"error occured in /start {e}", 500

async def chargeCard():
    return await asyncio.sleep(3)


@app.get('/_/health')
async def health():
    return 'OK'

@app.post('/onCall')
async def onCall():
    try:
        body = json.loads(request.data)
        session = neru.createSession()
        voice = Voice(session)
        messaging = Messages(session)
        state = State(session, f'application:{session.id}')

        vapiEventParams = VapiEventParams()
        vapiEventParams.callback = 'onEvent'
        vapiEventParams.vapiUUID = body['uuid']

        await voice.onVapiEvent(vapiEventParams).execute()

        fromContact = MessageContact()
        fromContact.type_keyword_ = 'sms'
        fromContact.number = body['from']

        toContact = MessageContact()
        toContact.type_keyword_ = 'sms'
        toContact.number = contact['number']

        await messaging.listenMessages(fromContact, toContact, 'onMessage').execute()

        await state.set("calldata", {
            'callUUID': body['uuid'],
            'flowState': 'parkid'
        })

        return jsonify([
            {
                'action': 'talk',
                'text': 'Welcome to VonagePark, enter the car park ID, followed by a hash to continue',
                'bargeIn': True
            },
            {
                'action': 'input',
                'type': ['dtmf'],
                'dtmf': {
                    'timeOut': '10',
                    'submitOnHash': True
                }
            }
        ])

    except Exception as e:
        print(e)
        return 'error'


@app.post('/onEvent')
async def onEvent():
    try:
        if not request.data:
            return 'request.data is not found', 400

        body = json.loads(request.data)

        if ('dtmf' in body):
            session = neru.getSessionFromRequest(request)
            state = State(session, f'application:{session.id}')
            messaging = Messages(session)

            fromNumber = body['from']

            toContact = MessageContact()
            toContact.type_keyword_ = 'sms'
            toContact.number = fromNumber

            vonageContact = MessageContact()
            vonageContact.type_keyword_ = 'sms'
            vonageContact.number = contact['number']

            digits = body['dtmf']['digits']

            callDataStr = await state.get("calldata")
            data = json.loads(callDataStr)

            if data['flowState'] == 'parkid':
                data['flowState'] = 'duration'
                data['parkingID'] = digits
                await state.set("calldata", data)

                return jsonify([
                    {
                        'action': 'talk',
                        'text': f"You are parking at {digits}. Press a digit to choose how many hours you want to pay for.",
                        'bargeIn': True
                    },
                    {
                        'action': 'input',
                        'type': ['dtmf'],
                        'dtmf': {
                            'timeOut': '10',
                            'submitOnHash': True
                        }
                    }
                ])
            if data['flowState'] == 'duration':
                data['flowState'] = 'reg'
                data['duration'] = digits
                await state.set("calldata", data)

                await messaging.sendText(
                    vonageContact,
                    toContact,
                    "Please reply with your car's registration number"
                ).execute()

                return jsonify([
                    {
                        'action': 'talk',
                        'text': "You will receive a text from this number, reply with your car's registration number."
                    },
                    {
                        'action': 'stream',
                        'streamUrl': ["https://onhold2go.co.uk/song-demos/free/a-new-life-preview.mp3"],
                        'loop': "0"
                    }
                ])
            if data['flowState'] == 'pay':
                scheduler = Scheduler(session)
                await chargeCard()

                await messaging.sendText(
                    vonageContact,
                    toContact,
                    f"You are parking at {data['parkingID']} and have paid for {data['duration']} hours."
                ).execute()

                testTime = datetime.now() + timedelta(seconds=20)

                startAtParams = StartAtParams()
                startAtParams.startAt = testTime.strftime("%Y-%m-%dT%H:%M:%SZ")
                startAtParams.callback = 'parkingReminder'
                startAtParams.payload = {
                    'from': fromNumber
                }

                await scheduler.startAt(startAtParams).execute()

                return jsonify([
                    {
                        'action': 'talk',
                        'text': f"Your card has been charged for {data['duration']} hours. You will receive a text confirmation and a reminder when your parking is about to expire",
                    }
                ])
        else:
            print(body)
            return 'OK'
    except Exception as e:
        print(e)
        return 'error', 500


@app.post('/onMessage')
async def onMessage():
    try:
        if not request.data:
            return 'request.data is not found', 400
        body = json.loads(request.data)
        session = neru.getSessionFromRequest(request)
        voice = Voice(session)
        state = State(session, f'application:{session.id}')
        dataStr = await state.get("calldata")
        data = json.loads(dataStr)
        data['flowState'] = 'pay'
        data['reg'] = body['message']['content']['text']
        await state.set('calldata', data)

        ncco = {
            "action": "transfer",
            "destination": {
                "type": "ncco",
                "ncco": [
                    {
                        'action': 'talk',
                        'text': f"You've registered the car {data['reg']}. Enter your card number followed by a hash to pay.",
                        'bargeIn': "true"
                    },
                    {
                        'action': 'input',
                        'type': ['dtmf'],
                        'dtmf': {
                            'timeOut': '10',
                            'submitOnHash': "true"
                        }
                    }
                ]
            }
        }

        await voice.uploadNCCO(data['callUUID'], ncco).execute()

        return 'OK'
    except Exception as e:
        print(e)
        return e, 500


@app.post('/parkingReminder')
async def parkingReminder():
    try:
        if not request.data:
            return 'request.data is not found', 400
        body = json.loads(request.data)
        session = neru.getSessionFromRequest(request)
        state = State(session, f'application:{session.id}')
        messaging = Messages(session)
        fromNumber = body['from']
        dataStr = await state.get("calldata")
        data = json.loads(dataStr)
        toContact = MessageContact()
        toContact.type = "sms"
        toContact.number = fromNumber

        vonageNumber = MessageContact()
        vonageNumber.type = "sms"
        vonageNumber.number = contact.number

        await messaging.sendText(
            vonageNumber,
            toContact,
            f"Your parking at {data['parkingID']} is about to run out."
        ).execute()

        return 'OK'
    except Exception as e:
        print(e)
        return e, 500

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(listenForInboundCall())
    port = os.getenv('NERU_APP_PORT')
    app.run(host="localhost", port=port)
