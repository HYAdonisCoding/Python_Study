import logging
from logging import handlers

class Logger(object):
    def __init__(self, log_name, log_file='app.log', level=logging.INFO):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level)

        # Create file handler
        file_handler = handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
        file_handler.setLevel(level)

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
if __name__ == "__main__":
    # Example usage
    log = Logger('example_logger', 'example.log')
    logger = log.get_logger()
    
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.critical("This is a critical message.")
    try:
        1 / 0  # This will raise an exception
    except Exception as e:
        logger.exception("An exception occurred: %s", e)
        logger.error("This is an exception message.", e)
    logger.info("Logging completed.")