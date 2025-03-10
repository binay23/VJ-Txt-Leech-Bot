import logging
from logging.handlers import RotatingFileHandler

# Set up the logging configuration
logging.basicConfig(
    level=logging.INFO,  # Change this to DEBUG for more detailed logs during development
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Set pyrogram logger to show warnings and errors only
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Optionally, you can log something here to check the configuration is working
logging.info("Logging is set up successfully.")
