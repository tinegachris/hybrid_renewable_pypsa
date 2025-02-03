import logging
import os

class Logger_Setup:
    @staticmethod
    def setup_logger(name, log_file=None, level=logging.INFO):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        # If log_file is specified, create file handler
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.propagate = False
        return logger