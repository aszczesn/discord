import logging

def setup_logger(name: str, level=logging.INFO, log_file=None):
    """
    Configuresand returns a logger instance.

    Args:
        name (str): Name of the logger.
        level (int): Logging level (e.g., logging.INFO).
        log_file (str, optional): File to save logs. Logs to console if None.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    # Add console handler
    logger.addHandler(console_handler)

    # Optionally, add a file handler

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)

    return logger