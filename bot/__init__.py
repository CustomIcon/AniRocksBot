import logging
from configparser import ConfigParser

from bot.bot import bot

# Logging at the start to catch everything
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    handlers=[
        logging.StreamHandler()
    ]
)
LOGS = logging.getLogger(__name__)

name = 'bot'

# Extra details
__version__ = '0.0.1'
__author__ = 'pokurt'

# Global Variables
bot = bot(name)
