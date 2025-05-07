# Telegram Channel Navigation Bot

This bot helps you manage and navigate through t.me links from your Telegram channel. It provides commands to add, list, and remove links, making it easy to organize and access your channel's content.

## Setup

1. First, get your bot token:
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` command and follow the instructions
   - Copy the token provided by BotFather

2. Install the required dependencies:
   ```bash
   pip install python-telegram-bot aiosqlite
   ```

3. Initialize the database:
   ```bash
   python sqlite_init.py
   ```

4. Edit `bot.py` and replace `'YOUR_BOT_TOKEN'` with the token you received from BotFather

5. Run the bot:
   ```bash
   python bot.py
   ```

## Available Commands

- `/add <t.me link>` - Add a new t.me link to the database
- `/list` - View all saved links as clickable buttons
- `/remove <id>` - Remove a link by its ID

## Example Usage

1. Add a link:
   ```
   /add https://t.me/your_channel/123
   ```

2. List all links:
   ```
   /list
   ```

3. Remove a link:
   ```
   /remove 1
   ```

## Features

- Validates t.me links before adding them
- Stores links in SQLite database
- Provides inline buttons for easy navigation
- Simple and intuitive interface 