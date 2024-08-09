from functools import wraps
from tabulate import tabulate
from address_book import AddressBook, Record
from assistant_info import ASSISTANT_INFO_TABLE_HEADERS, ASSISTANT_INFO_TABLE_DATA
from helpers.logging_config import setup_logging
from helpers.pickle_utils import save_data, load_data


logger = setup_logging()


def input_error(func):
    """
    A decorator that wraps a function and catches common exceptions,
    returning a string message for each exception type.

    Args:
        * func (callable): The function to be decorated.

    Returns:
        * callable: The wrapped function which handles the following exceptions:
            - KeyError: Raised when a dictionary key is not found.
            - ValueError: Raised when a function receives an argument of the correct
                type but an inappropriate value.
            - IndexError: Raised when a sequence subscript is out of range.
            - Exception: Catches any other unexpected exceptions.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {str(e)}"
        except KeyError as e:
            return f"KeyError: {str(e)}"
        except IndexError as e:
            return f"IndexError: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return inner


@input_error
def parse_input(user_input: str):
    """
    A function that receives the row, breaks it into words,
    the first word leads to lower case and removes extra characters.

    Args:
        * user_input (str): The user input.
    Returns:
        * cmd (str): the first word of the string without spaces in lower case
        * args (list): the rest of the words in the string
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, book: AddressBook):
    """
    A function that adds a new contact to the Address book.

    Args:
        * args (list): the list of words after the command
        * book (AddressBook): AddressBook class instance
    Returns:
    * str: "Contact updated."
    """
    if len(args) < 2:
        raise ValueError("Name or number are missing. usage: add <name> <number>")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook):
    """
    A function that changes the phone number of an existing contact.

    Args:
        * args (list): the list of words after the command
        * book (AddressBook): AddressBook class instance

    Returns:
        * str: "Contact changed." if success and "No such name '{name}' was found" if
            failed.
    """
    if len(args) < 3:
        raise ValueError(
            "Some details are missing. usage: change <name> <old_number> <new_number>"
        )
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"No such name '{name}' was found")
    record.edit_phone(old_phone, new_phone)
    return "Contact changed."


@input_error
def show_phone(args: list, book: AddressBook):
    """
    A function that shows the phone number of a contact.

    Args:
        * args (list): the list of words after the command
        * book (AddressBook): AddressBook class instance

    Returns:
        * str: the phone number if found and "Contact not found." if failed.
    """
    if len(args) == 0:
        raise IndexError("Name is missing. usage: phone <name>")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    return "; ".join(p.value for p in record.phones)


@input_error
def list_all(book: AddressBook):
    """
    A function that lists all contacts, their phone numbers and birthday.

    Args:
        * book (AddressBook): AddressBook class instance

    Returns:
        * str: the list of contacts and their phone numbers.
    """
    if len(book.data.items()) == 0:
        raise IndexError("The Address book is empty.")
    headers = ['Address Book']
    return tabulate(book.data.items(), headers, tablefmt="presto", stralign="left")


@input_error
def delete_contact(args: list, book: AddressBook):
    """
    A function that deletes contact from the Address book by name.

    Args:
        * args (list): the list of words after the command
        * book (AddressBook): AddressBook class instance

    Returns:
       * str: "Contact successfully deleted." if success and "Contact {name} not found." if
            failed.
    """
    if len(book.data.items()) < 1:
        raise IndexError("Name is missing. usage: delete <name>")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    book.delete(name)
    return "Contact successfully deleted"


@input_error
def add_birthday(args: list, book: AddressBook):
    """
    A function that adds birthday to the existing contact.

    Args:
        * args (list): the list of words after the command
        * book (AddressBook): AddressBook class instance

    Returns:
       * str: "Contact updated." if success and "Contact {name} not found." if
            failed.
    """
    if len(args) < 2:
        raise IndexError("Some details are missing. usage: add-birthday <name> <birthday>")
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    record.add_birthday(birthday)
    return "Contact updated"


@input_error
def show_birthday(args: list, book: AddressBook):
    """
    A function that shows birthday by the contact name.

    Args:
        * args (list): the list of words after the command
        * book (AddressBook): AddressBook class instance

    Returns:
       * str: birthday in the format DD.MM.YYYY
    """
    if len(args) < 1:
        raise IndexError("Name is missing. usage: show-birthday <name>")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    birthday = record.get_birthday()
    if birthday is None:
        raise KeyError(f"Contact {name} has no birthday.")
    return birthday


@input_error
def birthdays(book: AddressBook):
    """
    A function that shows birthday in the next 7 days.

    Args:
        * book (AddressBook): AddressBook class instance

    Returns:
       * str: table with birthdays
    """
    birthdays = book.get_upcoming_birthdays()
    if len(birthdays) == 0:
        raise IndexError("No contacts that need to be congratulated by day next week.")
    headers = ["Name", "Congratulation date"]
    table_data = [[key["name"], key["congratulation_date"]] for key in birthdays]
    return tabulate(table_data, headers, tablefmt="presto", stralign="left")


def assistant_info():
    """
    A function that shows all info about bot commands.
    """
    return tabulate(
        ASSISTANT_INFO_TABLE_DATA,
        ASSISTANT_INFO_TABLE_HEADERS,
        tablefmt="mixed_grid",
        stralign="left",
    )


def main():
    """
    This is a simple phonebook application.
    """
    book = load_data()
    print("Welcome to the assistant bot!")
    print("The table below summarizes information about the commands. But if you forget something in the process, just call the 'info' command and you will see this table again.")
    print(assistant_info())
    print()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "info":
            print(assistant_info())

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "all":
            print(list_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
