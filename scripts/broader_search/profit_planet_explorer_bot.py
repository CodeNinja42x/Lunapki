import logging
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = '6533439963:AAGjIK-Q8-qGYhdZgMUTjImBSKbzU5bzWLo'

# Start command
async def start(update: Update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi there! Welcome to Profit Planet Explorer Bot!')

# Fact command
async def fact(update: Update, context):
    """Send a random space fact when the command /fact is issued."""
    space_facts = [
        "The Sun makes up more than 99% of the total mass of the Solar System.",
        "Venus spins backwards compared to most planets in our solar system.",
        "A day on Venus is longer than its year.",
        "Mars has the tallest volcano and the deepest valley in the entire solar system.",
        "Jupiter's Great Red Spot is a storm that has been ongoing for at least 300 years.",
        "Saturn could float in water because it's primarily made of hydrogen and helium.",
        "Uranus spins on its side with a tilt of nearly 98 degrees.",
        "Pluto was discovered on February 18, 1930, by Clyde Tombaugh.",
        "The Moon is moving away from Earth at a rate of about 3.8 cm per year.",
        "There are more stars in the universe than grains of sand on Earth."
    ]
    fact = random.choice(space_facts)
    await update.message.reply_text(f"🚀 Here's your space fact: {fact}")

# Main function
async def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fact", fact))

    # Initialize the application (explicitly calling the initialize function)
    await application.initialize()

    # Start polling for updates
    logger.info("Bot is running... good vibes are flowing! 🌟")
    await application.start()
    await application.updater.start_polling()  # Start polling

    # Keep the bot running
    await application.updater._update_fetcher()

# Entry point for the script
if __name__ == "__main__":
    try:
        asyncio.run(main())  # Run the event loop
    except Exception as e:
        logger.error(f"Error occurred: {e}")
