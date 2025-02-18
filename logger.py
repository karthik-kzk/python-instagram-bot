import logging



logging.basicConfig(filename="errors.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def logError(e):
    logging.error(f"Exception occurred: {e}")
