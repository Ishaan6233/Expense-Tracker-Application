import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

EXPENSE_FILE = 'expenses.json'

class Expense:
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return self.__dict__

class ExpenseTracker:
    def __init__(self):
        self.expenses = self.load_expenses()

    def load_expenses(self):
        if os.path.exists(EXPENSE_FILE):
            with open(EXPENSE_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_expenses(self):
        with open(EXPENSE_FILE, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, description):
        expense = Expense(amount, category, description).to_dict()
        self.expenses.append(expense)
        self.save_expenses()
        print(f'Expense of {amount} added.')

    def view_expenses(self, filter_by=None, filter_value=None):
        filtered_expenses = self.expenses
        if filter_by and filter_value:
            filtered_expenses = [expense for expense in self.expenses if expense[filter_by] == filter_value]

        if not filtered_expenses:
            print("No expenses found.")
            return

        for i, expense in enumerate(filtered_expenses, start=1):
            print(f"{i}. {expense['amount']} - {expense['category']} - {expense['description']} - {expense['date']}")

    def edit_expense(self, expense_id, amount=None, category=None, description=None):
        if 0 < expense_id <= len(self.expenses):
            if amount:
                self.expenses[expense_id - 1]['amount'] = amount
            if category:
                self.expenses[expense_id - 1]['category'] = category
            if description:
                self.expenses[expense_id - 1]['description'] = description
            self.save_expenses()
            print("Expense updated.")
        else:
            print("Invalid expense ID.")

    def delete_expense(self, expense_id):
        if 0 < expense_id <= len(self.expenses):
            self.expenses.pop(expense_id - 1)
            self.save_expenses()
            print("Expense deleted.")
        else:
            print("Invalid expense ID.")

    def generate_report(self):
        category_totals = {}
        for expense in self.expenses:
            category = expense['category']
            amount = float(expense['amount'])
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

        print("\nExpense Report:")
        for category, total in category_totals.items():
            print(f"{category}: {total}")

    def visualize_data(self):
        categories = [expense['category'] for expense in self.expenses]
        amounts = [float(expense['amount']) for expense in self.expenses]

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.title('Expenses by Category')

        plt.subplot(1, 2, 2)
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution')

        plt.tight_layout()
        plt.show()

def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker")
        print("1. Add an expense")
        print("2. View expenses")
        print("3. Edit an expense")
        print("4. Delete an expense")
        print("5. Generate report")
        print("6. Visualize data")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(amount, category, description)
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            expense_id = int(input("Enter expense ID to edit: "))
            amount = input("Enter new amount (or leave blank to keep current): ")
            category = input("Enter new category (or leave blank to keep current): ")
            description = input("Enter new description (or leave blank to keep current): ")
            tracker.edit_expense(expense_id, amount, category, description)
        elif choice == '4':
            expense_id = int(input("Enter expense ID to delete: "))
            tracker.delete_expense(expense_id)
        elif choice == '5':
            tracker.generate_report()
        elif choice == '6':
            tracker.visualize_data()
        elif choice == '7':
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    main()
