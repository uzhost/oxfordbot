import telegram
import requests
import json

# Define your API key and base URL for the Oxford Dictionary API
APP_ID = 'your_app_id_here'
APP_KEY = 'your_app_key_here'
BASE_URL = 'https://od-api.oxforddictionaries.com/api/v2/entries/en/'

# Define your Telegram bot token
TOKEN = 'your_bot_token_here'

# Define the start message for the bot
START_MSG = "Welcome to the Dictionary Bot! Type /define <word> to get its definition, or type /wordoftheday to get the word of the day."

# Set up a connection to the Telegram API
bot = telegram.Bot(TOKEN)

# Define the function to handle incoming messages
def handle_message(update, context):
    # Get the text of the user's message
    message_text = update.message.text
    
    # Check if the user wants to get the word of the day
    if message_text == '/wordoftheday':
        # Call the Oxford Dictionary API to get the word of the day
        response = requests.get(BASE_URL + 'random', headers={'app_id': APP_ID, 'app_key': APP_KEY})
        if response.status_code == 200:
            # Parse the JSON response to get the word and definition
            data = json.loads(response.text)
            word = data['id']
            definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
            # Send the word and definition to the user
            update.message.reply_text(f"Word of the day: {word}\nDefinition: {definition}")
        else:
            update.message.reply_text("Sorry, there was an error getting the word of the day.")
            
    # Check if the user wants to define a word
    elif message_text.startswith('/define'):
        # Get the word the user wants to define
        word = message_text.split()[1]
        # Call the Oxford Dictionary API to get the definition of the word
        response = requests.get(BASE_URL + word.lower(), headers={'app_id': APP_ID, 'app_key': APP_KEY})
        if response.status_code == 200:
            # Parse the JSON response to get the definition
            data = json.loads(response.text)
            definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
            # Send the definition to the user
            update.message.reply_text(f"Definition of {word}: {definition}")
        else:
            update.message.reply_text(f"Sorry, I couldn't find a definition for {word}.")
    
    # If the user sends any other message, send the start message
    else:
        update.message.reply_text(START_MSG)

# Set up a handler for incoming messages
handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message)
dispatcher = telegram.ext.Dispatcher(bot, None)
dispatcher.add_handler(handler)

# Start the bot
bot_start_msg = "Dictionary Bot started. Type /start to begin."
print(bot_start_msg)
bot.send_message(chat_id=YOUR_CHAT_ID, text=bot_start_msg)
updater.start_polling()
