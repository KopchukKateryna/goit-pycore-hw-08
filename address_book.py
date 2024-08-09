from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """
    A base class for fields in a record.

    Attributes:
        * value (str): The value of the field.
    """

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    A class for storing a contact's name.
    Inherits from Field.
    """
    pass


class Phone(Field):
    """
    A class for storing a contact's phone number.

    Inherits from Field. Validates that the phone number is exactly 10 digits.
    """

    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """
    A class for storing a contact's birthday.

    Inherits from Field. Validates that the birthday is in the format DD.MM.YYYY and converts
    the string representation to a datetime object.

    Method:
        __init__(self, value: str): Initializes the birthday with a validated date.
    """

    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(birthday)
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc


class Record:
    """
    A class for storing contact information, including name and phone numbers.

    Attributes:
        * name (Name): The contact's name.
        * phones (list of Phone): A list of the contact's phone numbers.
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        """
        Adds a phone number to the contact's list of phone numbers.

        Args:
            * phone (str): The phone number to be added.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """
        Removes a phone number from the contact's list of phone numbers.

        Args:
            * phone (str): The phone number to be removed.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Edit an existing phone number in the contact's list of phone numbers.

        Args:
            * old_phone (str): The phone number to be replaced.
            * new_phone (str): The new phone number to replace the old one.
        """
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone: str):
        """
        Find a phone number in the contact's list of phone numbers.

        Args:
            * phone (str): The phone number to find.

        Returns:
            * Phone: The phone object if found, None otherwise.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        """
        Adds a birthday to the contact's list of birthdays.
        """
        self.birthday = Birthday(birthday)

    def get_birthday(self):
        """
        Returns birthday in DD.MM.YYYY format if success, and None if birthday doesn't exist
        """
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return None

    def __str__(self):
        birthday = None
        if self.birthday:
            birthday = self.birthday.value.strftime("%d.%m.%Y")
        birthday_row = f", Birthday: {birthday}" if birthday else ""
        return f"Phones: {'; '.join(p.value for p in self.phones)}{birthday_row}"


class AddressBook(UserDict):
    """
    A class for storing and managing contact records.

    Inherits from UserDict.
    """

    def add_record(self, record: Record):
        """
        Add a contact record to the address book.

        Args:
            * record (Record): The contact record to be added.
        """
        self.data[record.name.value] = record

    def find(self, name: str):
        """
        Find a contact record by name.

        Args:
            * name (str): The name of the contact to find.

        Returns:
            * Record: The contact record if found
        """
        return self.data.get(name)

    def delete(self, name: str):
        """
        Delete a contact record by name.

        Args:
            * name (str): The name of the contact to delete.
        """
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        """
        A function that identifies contact's with birthdays in the next 7 days, including today, and adjusts the congratulation
        date if the birthday falls on a weekend.
        Returns:
            * dict: A dictionary of contacts with their names and birthdays, with the congratulation date adjusted if
        """
        birthdays = []
        date_today = datetime.today().date()
        date_today_plus_week = date_today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                user_birthday = record.birthday.value.date()
                user_birthday = user_birthday.replace(year=date_today.year)
                if date_today <= user_birthday <= date_today_plus_week:
                    if user_birthday.weekday() in [5, 6]:
                        user_birthday += timedelta(days=(7 - user_birthday.weekday()))

                    birthdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": user_birthday.strftime("%d.%m.%Y"),
                        }
                    )
        return birthdays
