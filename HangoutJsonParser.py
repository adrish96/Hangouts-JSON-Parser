#!/usr/bin/python
import argparse, json, os

def parseData():
    for i in range(0, len(jsonData['conversations'])):
        conversation = {}
        conversation['chatName'] = ""
        conversation['participants'] = getParticipants(jsonData['conversations'][i]['conversation']['conversation']['participant_data'])
        conversation['messages'] = []

        for event in jsonData['conversations'][i]['events']:
            message = {}
            message['sender'] = {}
            message['sender']['name'] = getName(event['sender_id']['gaia_id'], conversation['participants'])
            message['sender']['id'] = event['sender_id']['gaia_id']
            message['unixtime'] = (int(event['timestamp']))/1000000

            if 'chat_message' in event:
                # if it's a message(normal hangouts, image...)
                if 'segment' in event['chat_message']['message_content']:
                    # if it's a normal hangouts message
                    content = ""
                    for k in range(0, len(event['chat_message']['message_content']['segment'])):
                        if event['chat_message']['message_content']['segment'][k]['type'] == "TEXT":
                            content = content + event['chat_message']['message_content']['segment'][k]['text']
                        elif event['chat_message']['message_content']['segment'][k]['type'] == "LINK":
                            content = content + event['chat_message']['message_content']['segment'][k]['text']
                    message['content'] = content

            conversation['messages'].append(message)

        simpleJson.append(conversation)
        simpleJson[i]['chatName'] = chatName(i)


def getParticipants(participant_data):
    return [{
        'id': participant['id']['gaia_id'],
        'name': participant.get('fallback_name', participant['id']['gaia_id'])
    } for participant in participant_data]


def getName(pid, participants):
    for p in participants:
        if pid == p['id']:
            return p['name']
    return pid


def chatName(i):
    if (('name' in jsonData['conversations'][i]['conversation']['conversation'])and(jsonData['conversations'][i]['conversation']['conversation']['name'] != "")):
        return jsonData['conversations'][i]['conversation']['conversation']['name']
    for participant in simpleJson[i]['participants']:
        if participant['id'] == jsonData['conversations'][i]['conversation']['conversation']['self_conversation_state']['self_read_state']['participant_id']['gaia_id']:
            return participant['name']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('INPUT_JSON_PATH', help='Path location of Hangouts.json file obtained from Google Takeout.')
    parser.add_argument('OUTPUT_DIRECTORY', help='Path to write output files.')
    args = parser.parse_args()

    jsonData = json.load(open(args.INPUT_JSON_PATH, 'r', encoding='utf-8'))
    simpleJson = []
    parseData()
    json.dump(simpleJson, open(os.path.join(args.OUTPUT_DIRECTORY, 'clean_hangoutsData.json'), 'w', encoding='utf-8'), indent=4)
