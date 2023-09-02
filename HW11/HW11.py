from collections import UserDict
from datetime import datetime, date
import re

class Field:
    def __init__(self, value=None):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

class Name(Field):
    def set_value(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        super().set_value(value)

class Phone(Field):
  
    def __init__(self, value=None):
        super().__init__(value)

    def set_value(self, value):
        if not self.is_valid_phone(value):
            print("Invalid phone number format")
        else:
            super().set_value(value)

    @staticmethod
    def is_valid_phone(phone_number):
        if not isinstance(phone_number, str):
            return False
        digits = "".join(filter(str.isdigit, phone_number))
        return 10 <= len(digits) <= 13

    def add_phone(self, phone_number):
        if not self.is_valid_phone(phone_number):
            print("Invalid phone number format")
        else:
            self.value = phone_number

    def remove_phone(self, phone_number):
        if phone_number in self.value:
            self.value.remove(phone_number)

class Birthday(Field):
    def set_value(self, value):
        if not self.is_valid_birthday(value):
            print("Invalid birthday format. Use 'YYYY-MM-DD'.")
        else:
            super().set_value(value)

    @staticmethod
    def is_valid_birthday(birthday):
        if not re.match(r'\d{4}-\d{2}-\d{2}', birthday):
            return False
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
# Перевіряю чи є запис ДН
    def has_birthday(self):
        return self.birthday is not None

    def add_phone(self, phone):
            if Phone(phone).is_valid_phone(phone):
                self.phones.append(Phone(phone))
                print(f"Phone {phone} is added to {self.name.get_value()}")
            else:
                print('Number is invalid. Chek the format')

    def remove_phone(self, phone):
        for p in self.phones:
            if p.get_value() == phone:
                self.phones.remove(p)
                break

    def change_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.get_value() == old_phone:
                p.set_value(new_phone)
                return f"Phone number '{old_phone}' for '{self.name.get_value()}' updated to '{new_phone}'."
        return f"Phone number '{old_phone}' not found for '{self.name.get_value()}'."

    def days_to_birthday(self):
        if self.birthday.get_value():
            today = date.today()
            birth_date = datetime.strptime(self.birthday.get_value(), '%Y-%m-%d').date()
            next_birthday = datetime(today.year, birth_date.month, birth_date.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day).date()
            days_until_birthday = (next_birthday - today).days
            return days_until_birthday
        return None

class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.get_value()] = record

    def search_by_name(self, name):
        found_records = []
        for record in self.data.values():
            if record.name.get_value().lower() == name.lower():
                found_records.append(record)
        return found_records

    def iterator(self, page_size=3):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0

        while current_index < total_records:
            yield records[current_index:current_index + page_size]
            current_index += page_size

def main():
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").lower()

        if command in ["hello", "hi"]:
            print("How can I help you?")

        elif command.startswith("add "):
            _, name, phone = command.split(" ", 2)
            if name and phone:
                record = Record(name)
                record.add_phone(phone)
                address_book.add_record(record)
            else:
                print("Please provide both name and phone number.")

        elif command.startswith("find "):
            _, name = command.split(" ", 1)
            if name:
                found_records = address_book.search_by_name(name)
                if found_records:
                    print("------------------------------------------------------------------------------------------------")
                    for record in found_records:
                        print(f"Name: {record.name.get_value()}")
                        for phone in record.phones:
                            print(f"Phone: {phone.get_value()}")
                    
                    print("------------------------------------------------------------------------------------------------")
                else:
                    print(f"No records found with name '{name}'.")
            else:
                print("Please provide a name to search for.")

        elif command.startswith("birthday "):
            _, name, birthday = command.split(" ", 2)
            if name and birthday:
                found_records = address_book.search_by_name(name)
                if found_records:
                    for record in found_records:
                        record.birthday.set_value(birthday)
                        # print(f"Birthday for '{record.name.get_value()}' set to '{birthday}'.")
                else:
                    print(f"No records found with name '{name}'.")
            else:
                print("Please provide both name and birthday in 'YYYY-MM-DD' format.")

        elif command.startswith("change "):
            _, name, phone = command.split(" ", 2)
            if name and phone:
                result = address_book.change_phone(name, phone)
                print(result)
            else:
                print("Please provide both name and phone number.")

        elif command == "show all":
            if address_book.data:
                for page, records in enumerate(address_book.iterator(), 1):
                    print(f"Page {page}:")
                    for record in records:
                        ("------------------------------------------------------------------")
                        print(f"Name: {record.name.get_value()}")
                        for phone in record.phones:
                            print(f"Phone: {phone.get_value()}")
                    if record.has_birthday():
                        print(f"Birthday: {record.birthday.get_value()}")
                    print("------------------------------------------------------------------")
            else:
                print("No contacts saved.")

        elif command == "days to birthday":
            name = input("Enter the name for checking days to birthday: ")
            if name:
                found_records = address_book.search_by_name(name)
                if found_records:
                    for record in found_records:
                        days = record.days_to_birthday()
                        if days is not None:
                            print(f"Days to birthday for '{record.name.get_value()}': {days} days.")
                        else:
                            print(f"'{record.name.get_value()}' does not have a valid birthday.")
                else:
                    print(f"No records found with name '{name}'.")
            else:
                print("Please provide a name to check days to birthday.")

        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break

        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
