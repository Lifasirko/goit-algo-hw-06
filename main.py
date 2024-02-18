from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = phones if phones is not None else []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return True
        return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me the correct name and phone please."
        except IndexError:
            return "Provide enough arguments."

    return inner


@input_error
def add_contact(contacts, *args):
    if len(args) < 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(contacts, *args):
    if len(args) < 2:
        raise ValueError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(contacts, *args):
    if not args:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(contacts, *args):
    return "\n".join([f"{name}: {number}" for name, number in contacts.items()])


def main():
    contacts = {}
    print("Welcome to the assistant bot! Type 'exit' or 'close' to quit.")

    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command.lower() in ["exit", "close"]:
            print("Good bye!")
            break
        elif command.lower() == "hello":
            print("How can I help you?")
        elif command.lower() == "add":
            print(add_contact(contacts, *args))
        elif command.lower() == "change":
            print(change_contact(contacts, *args))
        elif command.lower() == "phone":
            print(show_phone(contacts, *args))
        elif command.lower() == "all":
            print(show_all(contacts, *args))
        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()
