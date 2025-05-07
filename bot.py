import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import aiosqlite

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Regular expression for t.me links
TME_LINK_PATTERN = r'https?://t\.me/[a-zA-Z0-9_]+/\d+'

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a new link to the database."""
    if not context.args:
        await update.message.reply_text('Please provide a t.me link: /add <t.me link>')
        return

    url = context.args[0]
    if not re.match(TME_LINK_PATTERN, url):
        await update.message.reply_text('Please provide a valid t.me link')
        return

    async with aiosqlite.connect('links.db') as db:
        await db.execute('INSERT INTO links (url) VALUES (?)', (url,))
        await db.commit()
    
    await update.message.reply_text('Link added successfully!')

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all links as inline buttons."""
    async with aiosqlite.connect('links.db') as db:
        async with db.execute('SELECT id, url FROM links') as cursor:
            links = await cursor.fetchall()

    if not links:
        await update.message.reply_text('No links found in the database.')
        return

    keyboard = []
    for link_id, url in links:
        keyboard.append([InlineKeyboardButton(f"Link {link_id}", url=url)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Available links:', reply_markup=reply_markup)

async def remove_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a link from the database by ID."""
    if not context.args:
        await update.message.reply_text('Please provide a link ID: /remove <id>')
        return

    try:
        link_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text('Please provide a valid numeric ID')
        return

    async with aiosqlite.connect('links.db') as db:
        cursor = await db.execute('DELETE FROM links WHERE id = ?', (link_id,))
        await db.commit()
        
        if cursor.rowcount > 0:
            await update.message.reply_text(f'Link {link_id} removed successfully!')
        else:
            await update.message.reply_text(f'No link found with ID {link_id}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the Mini App button when the command /start is issued."""
    # Replace this URL with your deployed web app URL
    WEBAPP_URL = "https://your-app-name.onrender.com"  # Change this to your actual deployed URL
    keyboard = [[InlineKeyboardButton("Open Navigation", web_app=WebAppInfo(url=WEBAPP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Click the button below to open the navigation app:', reply_markup=reply_markup)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    # Replace the string below with your actual bot token from @BotFather
    application = Application.builder().token('7719549837:AAF_SWnaRIB3RxzsTEPbV5_SMysYr5ERHEA').build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_link))
    application.add_handler(CommandHandler("list", list_links))
    application.add_handler(CommandHandler("remove", remove_link))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main() 