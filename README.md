# AI Telegram Bot 🤖💬

## Project Description 📖

This is a **Telegram Bot** built with **aiogram** and **OpenRouter** that allows you to interact with a custom AI character. Unlike other similar bots, this bot has no censorship, is fully modular, and customizable. It's highly efficient, lightweight in terms of hosting requirements, and doesn’t overload the system. 🌍⚡

The goal of this project is to provide a fun and engaging AI character interaction experience for users, with no limitations, allowing complete freedom in how you interact with the character. Additionally, the bot is optimized to keep hosting costs extremely low. 💸

## Why I Created This Bot 🎈
I created this bot for fun and to boost activity in chats. It was developed in a single day to provide a unique and exciting experience for users to interact with AI characters without restrictions. Let's make chatting more fun and spontaneous!

## Installation Instructions ⚙️
Follow these steps to install and run the bot:

### 1. Clone the repository:
```bash
git clone https://github.com/your-repository-url.git
cd your-repository-directory
```

### 2. Create a Python virtual environment 🌱:
```bash
python3 -m venv venv
```

### 3. Activate the virtual environment 🔌:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install dependencies 📦:
```bash
pip install -r requirements.txt
```

### 5. Configure the bot 🔑:
Copy .env.example to .env:
```bash
cd resources
cp .env.example .env
```
Open .env and fill in the required information.

*If you want the bot to use stickers, name each sticker with a short description, convert them to .webp format, and place them in the resources/stickers folder.* 🖼️

### 6. Configure the AI Character bot uses 📝:
Copy system-prompt.txt.example to system-prompt.txt:
```bash
cp system-prompt.txt.example system-prompt.txt
```
*Find any AI character card online, paste its contents there, and save it as system-prompt.txt.*

### 7. Run the bot 🚀:
Now you can run the bot with the following command:
```bash
python main.py
```

## Contributions 🤝

Feel free to fork this repository, create pull requests, and contribute to the development of the project. All improvements, bug fixes, and feature suggestions are welcome! 


## License 📜

This project is licensed under the MIT License - see the LICENSE file for details.
