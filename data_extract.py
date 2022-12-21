from config import name, api_id, api_hash, phone
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from datetime import datetime, timedelta
import json

with TelegramClient(name, api_id, api_hash) as client:
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    chat = ''
    data = []

    day_ago = datetime.now() - timedelta(1) # get datetime 24 hours ago
    yesterday = datetime.strftime(day_ago, '%Y-%m-%d 00:00:00') # convert to str, set 00:00:00
    date_object = datetime.strptime(yesterday, '%Y-%m-%d 00:00:00').date()

    for message in client.iter_messages(chat, offset_date=date_object, reverse=True):
        try:
            text = message.text.strip()
            date = str(message.date).split('+')[0].strip()
            comments = message.replies.replies
            views = message.views
            forwards = message.forwards
        except:
            continue
        try:
            reactions = message.reactions.results
            reaction_data = []
            for reaction in reactions:
                reaction_data.append({
                    reaction.reaction: reaction.count
                })
        except:
            continue

        media_name = date.replace(" ", "_").replace("-", "_").replace(":", "_")
        download = message.download_media(f'data/{media_name}')

        if text != None and text != '':
            data.append({
                'channel': chat,
                'date_time': date,
                'message': text,
                'views': views,
                'comments': comments,
                'forwards': forwards,
                'reactions': reaction_data
            })

    with open('data.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
