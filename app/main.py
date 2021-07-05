import time
from pathlib import Path
from config import Config
from main_app import MainApp
import logging


def main():
    config = Config()

    debug = logging.INFO
    if config.contains("GENERAL", "debug"):
        debug_string = config.get("GENERAL", "debug")
        if "TRUE" in debug_string.upper():
            debug = logging.DEBUG

    # Make a directory to put logs in if one doesn't exist
    Path("logs").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(filename=f'logs\\{time.strftime("%m_%d_%Y")}.log',
                        level=debug,
                        format='%(asctime)s[%(levelname)s]: %(message)s')

    logging.info("Starting app")
    app: MainApp = MainApp(config)
    app.start()


if __name__ == '__main__':
    main()

