import re
import random
import os
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values("resources/.env")
TOKEN = config['TELEGRAM_BOT_TOKEN']
CHAT_ID = int(config['TELEGRAM_CHAT_ID'])
USERNAME = config['TELEGRAM_BOT_USERNAME']
OPENROUTER_TOKEN = config['OPENROUTER_TOKEN']
API_URL = config['API_URL']
AI_MODEL = config['AI_MODEL']
CHAR_NAME = config['CHARACTER_NAME']
MAIN_MSG = str(config['MAIN_MSG'])
PROMPT_CONSTRUCTOR_MEDIA = str(config['PROMPT_CONSTRUCTOR_MEDIA'])
PROMPT_CONSTRUCTOR_STICKER = str(config['PROMPT_CONSTRUCTOR_STICKER'])
ERROR_MSG = str(config['ERROR_MSG'])
STICKERS_MSG = str(config['STICKERS_MSG'])
LIMIT_EXCEEDED_MSG = str(config['LIMIT_EXCEEDED_MSG'])

# Function to costruct the prompt to AI
def construct_prompt(message, openai_text_api_format=False, openai_vision_api_format=False) -> str:
    """Construct the prompt to AI"""

    def scrape_message_text(message) -> str:
        """Scrape the text from the message"""
        if message.text: return message.text
        if message.caption: return f"*{PROMPT_CONSTRUCTOR_MEDIA}*\n" + message.caption
        if message.sticker: return f"*{PROMPT_CONSTRUCTOR_STICKER}*\n" # We don't handle the stickers from user, but from the bot
        return None

    messages = [message]
    counter = 1  # Start with 1 because the initial message is already included
    while message.reply_to_message and counter < 6:
        message = message.reply_to_message
        messages.append(message)
        counter += 1
    
    chat_history = []
    for msg in reversed(messages):
        name = msg.from_user.full_name
        text = scrape_message_text(msg)
        if not text: continue

        if USERNAME in text:
            text = text.replace(f"@{USERNAME}", f"{CHAR_NAME},")

        if not msg.from_user.username == USERNAME: chat_history.append(f"User ({name}): {text}")
        else: chat_history.append(f"{CHAR_NAME}: {text}")
    
    chat_history.append(f"{CHAR_NAME}: ")

    stickers = [os.path.splitext(f)[0] for f in os.listdir("resources/stickers") if f.endswith(".webp")]

    with open("resources/system-prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = MAIN_MSG.format(character=f"\"{file.read()}\".")
    stickers_msg = STICKERS_MSG.format(stickers=", ".join(stickers), random_sticker=random.choice(stickers)) if stickers else ""
    prompt = "\n\n".join(chat_history)

    if openai_text_api_format: return [
        {"role": "system", "content": f"{system_prompt} {stickers_msg}"},
        {"role": "user", "content": prompt},
    ]

    if openai_vision_api_format: return [
        {"role": "system", "content": [{"type": "text", "text": f"{system_prompt} {stickers_msg}"}]},
        {"role": "user", "content": [{"type": "text", "text": prompt}]},
    ]
    
    return f"{system_prompt} {stickers_msg}\n\n{prompt}" 

# Function to format the response from AI
def format_message(response) -> str:
    """Format the response from AI"""

    def remove_namings(text: str, name: str) -> str:
        """Remove namings from the text (AKA the name of the character: text)"""

        def generate_namings(name: str) -> list:
            """Additional func. to generate namings from character name"""
            parts = name.split()
            namings = [f"{name}: "]

            if len(parts) > 1:
                namings.append(f"{parts[-1]} " + " ".join(parts[:-1]) + ": ")
            
            for part in parts:
                namings.append(f"{part}: ")
            
            return namings
        
        namings = generate_namings(name)
        pattern = "|".join(re.escape(n) for n in namings)
        return re.sub(pattern, "", text, flags=re.IGNORECASE)

    formatted_message = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', response)  # **text** -> <b>text</b>
    formatted_message = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_message)  # *text* -> <i>text</i>
    formatted_message = re.sub(r'\[(.*?)\]', r'<i>\1</i>', formatted_message)  # [text] -> <i>text</i>
    formatted_message = re.sub(r'\((.*?)\)', r'<i>\1</i>', formatted_message)  # (text) -> <i>text</i>
    formatted_message = re.sub(r'\/\/(.*?)\/\/', r'<i>\1</i>', formatted_message)  # //text// -> <i>text</i>

    formatted_message = remove_namings(formatted_message, CHAR_NAME)
    
    sticker_matches = re.findall(r'==([^=]+)==', formatted_message)
    if sticker_matches:
        formatted_message = re.sub(r'==([^=]+)==', "", formatted_message)
        sticker_paths = [f"resources/stickers/{match}.webp" for match in sticker_matches]

    if not formatted_message: formatted_message = "..."    
    
    if sticker_matches and os.path.exists(sticker_paths[-1]) and random.randint(0, 2) == 1: return formatted_message, sticker_paths[-1]
    return formatted_message, False

# Custom filter for messages
def custom_filter(message) -> bool:
    """Custom filter for aiogram, to handle cases when bot needs to answer to them"""
    if message.chat.id != CHAT_ID:
        return False
    
    if not message.text and not message.caption:
        return False

    # Check random chance first
    if random.randint(1, 50) == 1:
        return True
    
    # Check if the bot username is mentioned
    if f"@{config['TELEGRAM_BOT_USERNAME']}" in message.text:
        return True
    
    # Check if the message is a reply to a message from the bot
    return message.reply_to_message and message.reply_to_message.from_user.username == config['TELEGRAM_BOT_USERNAME']