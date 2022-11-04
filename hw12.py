import pickle
import os
import datetime
from collections import UserDict


def now():
    return datetime.today()


def create_date(*, year, month, day):
    return datetime(year=year, month=month, day=day).date()


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

   
    def __repr__(self) -> str:
        return self.value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        self.__value = value

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str = '') -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        if len(value) >= 10:  # phone format!!!
            self.__value = value
        else:
            print('Enter right phone number, please!')

    def __str__(self) -> str:
        return self.value


class Birthday(Field):
    def __init__(self, value: str = '') -> None:
        super().__init__(value)

    def to_datetime(self):
        self.value=datetime.strptime(self.value, '%d.%m.%Y')    

    @property
    def value(self) -> datetime.date:
        return self.__value

    @value.setter
    def value(self, value):
        value_list=value.split(".")
        if len(value_list[0])==2 and len(value_list[1])==2 and len(value_list[2])==4:  
                self.__value = value
        else:
            raise ValueError

    def __str__(self) -> str:
        return self.value
  

class Record(UserDict):
    def __init__(self, name: Name, phone, birthday: Birthday = None):
        self.name: Name = name
        self.phone:Phone = phone
        if phone is not None:
            self.phones=[phone]
        else:
            self.phones=[]
        self.birthday = birthday
        self.data = {'name': self.name,
                     "phones": self.phones, "birthday": self.birthday}   

    
    def days_to_birthday(self):
        # self.now = now()
        if self.birthday is not None:
            birthday: datetime.date = self.birthday.value.date()
            next_birthday = create_date(
                year=now.year, month=birthday.month, day=birthday.day
            )
            if birthday < next_birthday:
                next_birthday = create_date(
                    year=next_birthday.year + 1,
                    month=next_birthday.month,
                    day=next_birthday.day,
                )
            return (next_birthday - birthday).days
        return None

 
    def add_phone(self, new_phone: Phone):
        self.phones.append(new_phone)
        return self.phones   


    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)
          

    def del_phone(self, old_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone.value:
                return self.phones.pop(i)


class Iterator:
    def __init__(self):
        self.counter=0

    def __next__(self):
        if self.counter<10:
            self.counter+=1
            return self.counter
        raise StopIteration  

    def __repr__(self) -> str:
        return self.value
              

class AddressBook(UserDict):

    def __init__(self):
        self.data: dict = {}

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec

    def iterator(self):
        book=[self.data[key] for key in self.data]
        n=0
        while True:
            try:
                yield book[n:n+2]
                n+=2
            except:
                break 
          
  
contacts = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except (KeyError, ValueError, IndexError):
            return "Enter right name, phone or birthday, please!"

    return wrapper


def hello(_):
    return 'How can I help you?'


def exit(_):
    return 'Good bye'

def exit_from_book_handler(*args):
    with open("dump.pickle", "wb") as f:
        pickle.dump(contacts, f)
    return exit(*args)    


@input_error
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2])
    #birthday.to_datetime()
    rec = Record(name, phone, birthday)
    contacts.add_record(rec)
    return f'contact {name.value} {phone.value} {birthday.value} added successfully to addressbook {contacts}'
  
@input_error
def change(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = contacts.get(name.value)
    if rec:
        rec.change_phone(old_phone, new_phone)
        return f'Contact {name.value} changed successfully'

def get_phone(*args):
    name = Name(args[0])
    rec = contacts.get(name.value)
    if rec:
        return rec.phones
    return "No such contact"


def show_all(*args):
    print(contacts.iterator())
    return '\n'.join([f'{k}:{v}' for k, v in contacts.items()])


COMMANDS = {exit_from_book_handler: ['good bye', 'exit', 'close', 'bye', '.'], add: ['add', 'додай'], change: [
    'change', 'заміни'], get_phone: ['phone', 'номер'], show_all: ['show all', 'show'], hello: ['hello', 'hi']}


def parse_command(request: str):
    for k, v in COMMANDS.items():
        for i in v:
            if request.lower().startswith(i.lower()):
                return k, request[len(i):].strip().split(' ')


def main():

    while True:
        request = input('You: ')

        result, data = parse_command(request)
        print(result(*data))

        if result is exit_from_book_handler:
            break

if os.path.exists('dump.pickle'):
    with open('dump.pickle', 'rb') as f:
        contacts=pickle.load(f)
        #print(contacts)              

if __name__ == '__main__':
    main()
