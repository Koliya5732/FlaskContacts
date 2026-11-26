
import json
import os

from dataclasses import dataclass, asdict


# Модель одного контакта
@dataclass
class Contact:
    id: int
    name: str
    phone: str
    email: str


# Управление контактами
class ContactManager:

    def __init__(self):
        self.filename = os.path.join(
            os.path.dirname(__file__),
            "contacts.json"
        )
        self.contacts = []
        self.load_contacts()

    # Загрузка контактов из JSON
    def load_contacts(self):
        if not os.path.exists(self.filename):
            self.save_contacts()
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.contacts = [
                Contact(**item) for item in data
            ]

        except (json.JSONDecodeError, TypeError, KeyError):
            self.contacts = []

    # Сохранение контактов в JSON
    def save_contacts(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [asdict(contact) for contact in self.contacts],
                file,
                ensure_ascii=False,
                indent=4
            )

    # Добавление контакта
    def add_contact(self, name, phone, email):
        new_id = max(
            (contact.id for contact in self.contacts),
            default=0
        ) + 1

        contact = Contact(new_id, name, phone, email)

        self.contacts.append(contact)
        self.save_contacts()

    # Получение всех контактов
    def get_all_contacts(self):
        return self.contacts

    # Поиск контактов
    def search_contacts(self, query):
        query = query.lower()

        return [
            contact for contact in self.contacts
            if query in contact.name.lower()
            or query in contact.phone.lower()
        ]

    # Удаление контакта
    def delete_contact(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                self.contacts.remove(contact)
                self.save_contacts()
                return True

        return False
