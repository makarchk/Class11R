import json
import csv
import os
from datetime import datetime

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def validate_date(date_string, format_type="%d-%m-%Y"):
    try:
        datetime.strptime(date_string, format_type)
        return True
    except ValueError:
        return False


class Note:
    FILE_PATH = 'notes.json'

    def __init__(self, title, content):
        self.id = int(datetime.now().timestamp())
        self.title = title
        self.content = content
        self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return self.__dict__


class NotesManager:
    @staticmethod
    def create_note():
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")
        note = Note(title, content)
        notes = load_data(Note.FILE_PATH)
        notes.append(note.to_dict())
        save_data(Note.FILE_PATH, notes)
        print("Заметка успешно добавлена")

    @staticmethod
    def view_notes():
        notes = load_data(Note.FILE_PATH)
        if not notes:
            print("Нет заметок")
            return
        for note in notes:
            print(f"ID: {note['id']} | Заголовок: {note['title']} | Содержимое заметки: {note['content']} | Дата: {note['timestamp']}")

    @staticmethod
    def delete_note():
        note_id = input("Введите ID заметки для удаления: ")
        notes = load_data(Note.FILE_PATH)
        updated_notes = [note for note in notes if str(note['id']) != note_id]
        save_data(Note.FILE_PATH, updated_notes)
        print("Заметка удалена")

    @staticmethod
    def export_to_csv():
        notes = load_data(Note.FILE_PATH)
        file_name = input("Введите имя CSV-файла для импорта: ")
        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['id', 'title', 'content', 'timestamp'])
            writer.writeheader()
            writer.writerows(notes)
        print(f"Заметки экспортированы в {file_name}!")

    @staticmethod
    def import_from_csv_notes():
        file_name = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(file_name):
            print("Файл не найден.")
            return

        notes = load_data(Note.FILE_PATH)
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                note = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'content': row['content'],
                    'timestamp': row['timestamp']
                }
                notes.append(note)
        save_data(Note.FILE_PATH, notes)
        print("Заметки успешно импортированы!")


class Task:
    FILE_PATH = 'tasks.json'
    def __init__(self, title, description, done, priority, due_date):
        self.id = int(datetime.now().timestamp())
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self):
        return self.__dict__


class TasksManager:

    @staticmethod
    def create_task():
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        prior = input("Выберите приоритет (Высокий/Средний/Низкий): ")
        deadline = input("Введите срок выполнения (формат: DD-MM-YYYY): ")
        if not validate_date(deadline):
            print("Некорректная дата. Задача не дабавлена")
            return
        task = Task(title, description, 'not done', prior, deadline)
        tasks = load_data(Task.FILE_PATH)
        tasks.append(task.to_dict())
        save_data(Task.FILE_PATH, tasks)
        print("Задача успешно добавлена")

    @staticmethod
    def view_tasks():
        tasks = load_data(Task.FILE_PATH)
        if not tasks:
            print("Нет задач.")
            return
        for task in tasks:
            print(f"ID: {task['id']} | Приоритет: {task['priority']} | Описание: {task['description']} | Дедлайн: {task['due_date']} | Создано: {task['created_at']} | Статус задачи: {task['done']}")

    @staticmethod
    def mark_task_as_done():
        task_id = input("Введите ID выполненной задачи: ")
        tasks = load_data(Task.FILE_PATH)
        task_indicator = False
        for task in tasks:
            if str(task['id']) == task_id:
                task['done'] = 'done'
                task_indicator = True
                break
        if task_indicator:
            save_data(Task.FILE_PATH, tasks)
            print("Статус задачи изменен")
        else:
            print(f"Задача с ID: {task_id} не найдена")

    @staticmethod
    def delete_task():
        task_id = input("Введите ID задачи для удаления: ")
        tasks = load_data(Task.FILE_PATH)
        updated_tasks = [task for task in tasks if str(task['id']) != task_id]
        save_data(Task.FILE_PATH, updated_tasks)
        print("Задача удаленa")

    @staticmethod
    def export_to_csv_tasks():
        tasks = load_data(Task.FILE_PATH)
        file_name = input("Введите имя CSV-файла для импорта: ")
        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['id', 'title', 'description', 'done', 'priority', 'due_date', 'created_at'])
            writer.writeheader()
            writer.writerows(tasks)
        print(f"Заметки экспортированы в {file_name}!")

    @staticmethod
    def import_from_csv_tasks():
        file_name = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(file_name):
            print("Файл не найден.")
            return

        tasks = load_data(Task.FILE_PATH)
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                task = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'description': row['description'],
                    'done': row['done'],
                    'priority': row['priority'],
                    'due_date': row['due_date'],
                    'created_at': row['created_at']
                }
                tasks.append(task)
        save_data(Task.FILE_PATH, tasks)
        print("Задачи успешно импортированы!")


class Contact:
    FILE_PATH = 'contacts.json'
    def __init__(self, name, phone, email):
        self.id = int(datetime.now().timestamp())
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return self.__dict__


class ContactsManager:
    @staticmethod
    def add_contact():
        name = input("Введите имя: ")
        phone = input("Введите номер телефона ")
        email = input("Введите email: ")
        contact = Contact(name, phone, email)
        contacts = load_data(Contact.FILE_PATH)
        contacts.append(contact.to_dict())
        save_data(Contact.FILE_PATH, contacts)
        print("Контакт успешно добавлен")

    @staticmethod
    def search_contact():
        contacts = load_data(Contact.FILE_PATH)
        if not contacts:
            print("Нет контактов")
            return
        search_contact = input("Введите имя ИЛИ номер телефона: ")
        indicator = False
        for contact in contacts:
            if contact['name'] == search_contact or contact['phone'] == search_contact:
                print(f"Контакт успешно найден! ID: {contact['id']} | Имя: {contact['name']} | Телефон: {contact['phone']} | Email: {contact['email']}")
                indicator = True
                break
        if not indicator:
            print(f"Контакт {search_contact} не найден!")

    @staticmethod
    def delete_contact():
        contact_id = input("Введите ID контакта для удаления: ")
        contacts = load_data(Contact.FILE_PATH)
        updated_contacts = [contact for contact in contacts if str(contact['id']) != contact_id]
        save_data(Contact.FILE_PATH, updated_contacts)
        print("Контакт удалён")

    @staticmethod
    def export_to_csv_contacts():
        contacts = load_data(Contact.FILE_PATH)
        file_name = input("Введите имя CSV-файла для импорта: ")
        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['id', 'name', 'phone', 'email'])
            writer.writeheader()
            writer.writerows(contacts)
        print(f"Заметки экспортированы в {file_name}!")

    @staticmethod
    def import_from_csv_contacts():
        file_name = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(file_name):
            print("Файл не найден.")
            return

        contacts = load_data(Contact.FILE_PATH)
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                contact = {
                    'id': int(row['id']),
                    'name': row['name'],
                    'phone': row['phone'],
                    'email': row['email']
                }
                contacts.append(contact)
        save_data(Contact.FILE_PATH, contacts)
        print("Контакты успешно импортированы!")


class Finance:
    FILE_PATH = 'finance.json'
    def __init__(self, description, amount, date, category):
        self.description = description
        self.amount = amount
        self.date = date
        self.category = category

    def to_dict(self):
        return self.__dict__

class FinanceManager:

    @staticmethod
    def add_transaction():
        description = input("Введите описание транзакции: ")
        amount = float(input("Введите сумму транзакции: "))
        date = input("Введите дату (формат: DD-MM-YYYY): ")
        category = input('Введите категорию операции (например, "Еда", "Транспорт", "Зарплата"): ')
        transaction = Finance(description, amount, date, category)
        if not validate_date(date):
            print("Некорректная дата. Транзакция не добавлена")
            return
        transactions = load_data(Finance.FILE_PATH)
        transactions.append(transaction.to_dict())
        save_data(Finance.FILE_PATH, transactions)
        print("Транзакция добавлена")

    @staticmethod
    def view_transactions():
        transactions = load_data(Finance.FILE_PATH)
        if not transactions:
            print("Нет транзакций.")
            return
        for transaction in transactions:
            print(f"Описание: {transaction['description']} | Сумма: {transaction['amount']} | Дата: {transaction['date']} | Категория: {transaction['category']}")

    @staticmethod
    def export_to_csv_finance():
        transactions = load_data(Finance.FILE_PATH)
        file_name = input("Введите имя CSV-файла для импорта: ")
        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['description', 'amount', 'date', 'category'])
            writer.writeheader()
            writer.writerows(transactions)
        print(f"Заметки экспортированы в {file_name}!")

    @staticmethod
    def import_from_csv_finance():
        file_name = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(file_name):
            print("Файл не найден.")
            return

        transactions = load_data(Finance.FILE_PATH)
        with open(file_name, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                transaction = {
                    'description': row['description'],
                    'amount': float(row['amount']),
                    'date': row['date'],
                    'category': row['category']
                }
                transactions.append(transaction)
        save_data(Finance.FILE_PATH, transactions)
        print("Транзакции успешно импортированы!")

    @staticmethod
    def generate_report():
        start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
        end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")

        if not (validate_date(start_date) and validate_date(end_date)):
            print("Некорректные даты.")
            return

        transactions = load_data(Finance.FILE_PATH)
        filtered_transactions = [
            t for t in transactions
            if start_date <= t['date'] <= end_date
        ]

        if not filtered_transactions:
            print("Нет транзакций за указанный период.")
            return

        total_income = sum(t['amount'] for t in filtered_transactions if t['amount'] > 0)
        total_expenses = sum(abs(t['amount']) for t in filtered_transactions if t['amount'] < 0)
        balance = total_income - total_expenses

        print(f"Финансовый отчёт за период с {start_date} по {end_date}:")
        print(f"- Общий доход: {total_income:.2f} руб.")
        print(f"- Общие расходы: {total_expenses:.2f} руб.")
        print(f"- Баланс: {balance:.2f} руб.")

        report_file = f"report_{start_date}_{end_date}.csv"
        with open(report_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['description', 'amount', 'date', 'category'])
            writer.writeheader()
            writer.writerows(filtered_transactions)

        print(f"Подробная информация сохранена в файле {report_file}.")


class Calculator:
    @staticmethod
    def calculate():
        expression = input("Введите выражение:  ")
        try:
            result = eval(expression)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка вычисления: {e}")



def main_menu():
    while True:
        print('''
Добро пожаловать в Персональный помощник!
1. Управление заметками
2  Управление задачами
3. Управление контактами
4. Управление финансами
5. Калькулятор
6. Выход''')
        choice = input("Выберите действие: ")
        if choice == "1":
            notes_menu()
        elif choice == "2":
            tasks_menu()
        elif choice == "3":
            contacts_menu()
        elif choice == "4":
            finance_menu()
        elif choice == "5":
            Calculator.calculate()
        elif choice == "6":
            print("Выход из приложения.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова")
def notes_menu():
    while True:
        print('''
Управление заметками:
1. Добавить заметку
2. Посмотреть заметки
3. Удалить заметку
4. Экспорт заметок в CSV
5. Импорт заметок из CSV
6. Назад''')
        choice = input("Выберите действие: ")
        if choice == "1":
            NotesManager.create_note()
        elif choice == "2":
            NotesManager.view_notes()
        elif choice == "3":
            NotesManager.delete_note()
        elif choice == "4":
            NotesManager.export_to_csv()
        elif choice == "5":
            NotesManager.import_from_csv_notes()
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Попробуйте снова")


def tasks_menu():
    while True:
        print('''
Управление задачами:
1. Добавить новую задачу
2. Просмотреть задачи
3. Отметить задачу как выполненную
4. Удалить задачу
5. Создание CSV-файла
6. Импорт из CSV-файла
7. Назад
''')
        choice = input("Выберите действие: ")
        if choice == "1":
            TasksManager.create_task()
        elif choice == "2":
            TasksManager.view_tasks()
        elif choice == "3":
            TasksManager.mark_task_as_done()
        elif choice == "4":
            TasksManager.delete_task()
        elif choice == "5":
            TasksManager.export_to_csv_tasks()
        elif choice == "6":
            TasksManager.import_from_csv_tasks()
        elif choice == "7":
            break
        else:
            print("Некорректный выбор. Попробуйте снова")

def contacts_menu():
    while True:
        print('''
Управление контактами:
1. Добавить контакт
2. Поиск контакта по имени ИЛИ номеру телефона
3. Удалить контакт
4. Создание CSV-файла
5. Импорт из CSV-файла
6. Назад
''')
        choice = input("Выберите действие: ")
        if choice == "1":
            ContactsManager.add_contact()
        elif choice == "2":
            ContactsManager.search_contact()
        elif choice == "3":
            ContactsManager.delete_contact()
        elif choice == "4":
            ContactsManager.export_to_csv_contacts()
        elif choice == "5":
            ContactsManager.import_from_csv_contacts()
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Попробуйте снова")

def finance_menu():
    while True:
        print('''
Управление финансами:
1. Добавить транзакцию
2. Посмотреть транзакции
3. Создание CSV-файла 
4. Импорт CSV-файла
5. Генерация финансового отчета
6. Назад''')
        choice = input("Выберите действие: ")
        if choice == "1":
            FinanceManager.add_transaction()
        elif choice == "2":
            FinanceManager.view_transactions()
        elif choice == "3":
            FinanceManager.export_to_csv_finance()
        elif choice == "4":
            FinanceManager.import_from_csv_finance()
        elif choice == "5":
            FinanceManager.generate_report()
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Попробуйте снова")

if __name__ == "__main__":
    main_menu()    









