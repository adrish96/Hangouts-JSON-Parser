#!/usr/bin/python
import argparse, json, os

def parseData():
    for orig_conv in jsonData['conversations']:
        conversation = {
            'chatName': '',
            'participants': [
                {
                    'id': participant['id']['gaia_id'],
                    'name': participant.get('fallback_name', participant['id']['gaia_id'])
                }
                for participant in
                orig_conv['conversation']['conversation']['participant_data']
            ],
            'messages': []
        }

        for event in orig_conv['events']:
            message = {
                'sender': {
                    'name': getName(event['sender_id']['gaia_id'], conversation['participants']),
                    'id':   event['sender_id']['gaia_id']
                },
                'unixtime': int(event['timestamp'])/1000000
            }

            if 'chat_message' in event:
                # if it's a message(normal hangouts, image...)
                if 'segment' in event['chat_message']['message_content']:
                    # if it's a normal hangouts message
                    content = ""
                    for segment in event['chat_message']['message_content']['segment']:
                        if segment['type'] == "TEXT":
                            content = content + segment['text']
                        elif segment['type'] == "LINK":
                            content = content + segment['text']
                    message['content'] = content

            conversation['messages'].append(message)

        conversation['chatName'] = chatName(orig_conv, conversation['participants'])
        simpleJson.append(conversation)

def getName(pid, participants):
    for p in participants:
        if pid == p['id']:
            return p['name']
    return pid

def chatName(orig_conv, participants):
    if (('name' in orig_conv['conversation']['conversation']) and (orig_conv['conversation']['conversation']['name'] != "")):
        return orig_conv['conversation']['conversation']['name']
    for participant in participants:
        if participant['id'] == orig_conv['conversation']['conversation']['self_conversation_state']['self_read_state']['participant_id']['gaia_id']:
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
