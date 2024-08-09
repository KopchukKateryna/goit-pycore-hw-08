import pickle
from pathlib import Path
import logging

from address_book import AddressBook


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """
    Save data to a pickle file.

    Args:
        book (AddressBook): The object to be saved (e.g., an instance of AddressBook).
        filename (str): The name of the file to save the data to. Default is "addressbook.pkl".

    Raises:
        Exception: If an error occurs during the saving process, it will be logged.
    """
    try:
        with Path(filename).open("wb") as f:
            pickle.dump(book, f)
        logging.info("Data successfully saved to %s", filename)
    except Exception as e:
        logging.error("Error occurred while saving data to %s: %s", filename, e)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """
    Load data from a pickle file.

    Args:
        filename (str): The name of the file to load the data from. Default is "addressbook.pkl".

    Returns:
        Any: The loaded data, or a new instance of AddressBook if the file is not found or an error occurs.
    """
    file_path = Path(filename)
    if not file_path.exists():
        logging.warning(
            "File %s not found. Returning a new AddressBook instance.", filename
        )
        return AddressBook()

    try:
        with file_path.open("rb") as f:
            data = pickle.load(f)
        logging.info("Data successfully loaded from %s", filename)
        return data
    except (pickle.UnpicklingError, EOFError) as e:
        logging.error("Error occurred while loading data from %s: %s", filename, e)
        return AddressBook()
    except Exception as e:
        logging.critical(
            "Unknown error occurred while loading data from %s: %s", filename, e
        )
        return AddressBook()
