
from flask import Flask, render_template, request, redirect, url_for, flash

from models import ContactManager


# Создание Flask-приложения
app = Flask(__name__)
app.secret_key = "contacts-manager-secret-key"

# Подключение менеджера контактов
manager = ContactManager()


# Главная страница
@app.route("/")
def index():
    query = request.args.get("q", "").strip()

    if query:
        contacts = manager.search_contacts(query)
    else:
        contacts = manager.get_all_contacts()

    return render_template(
        "index.html",
        contacts=contacts,
        query=query
    )


# Добавление контакта
@app.route("/add", methods=["POST"])
def add_contact():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()

    # Проверка заполнения полей
    if not name or not phone or not email:
        flash("Заполните все поля!", "error")
        return redirect(url_for("index"))

    if len(name) < 2:
        flash("Имя должно содержать минимум 2 символа!", "error")
        return redirect(url_for("index"))

    if "@" not in email:
        flash("Введите корректный email!", "error")
        return redirect(url_for("index"))

    manager.add_contact(name, phone, email)

    flash("Контакт успешно добавлен!", "success")
    return redirect(url_for("index"))


# Удаление контакта
@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    if manager.delete_contact(contact_id):
        flash("Контакт удалён!", "success")
    else:
        flash("Контакт не найден!", "error")

    return redirect(url_for("index"))


# Запуск приложения
if __name__ == "__main__":
    app.run(debug=True)
