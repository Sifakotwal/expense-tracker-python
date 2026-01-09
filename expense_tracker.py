# Simple Expense Tracker

import csv
import os
from datetime import datetime


class ExpenseTracker:
    """Manage personal expenses with CSV storage"""
    
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.predefined_categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
        self._initialize_file()
    
    def _initialize_file(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Date', 'Amount', 'Category', 'Description'])
    
    def _get_next_id(self):
        """Get the next available ID"""
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                rows = list(reader)
                if rows:
                    return int(rows[-1][0]) + 1
                else:
                    return 1
        except Exception:
            return 1
    
    def add_expense(self, amount, category, description):
        """Add a new expense"""
        try:
            amount = float(amount)
            if amount <= 0:
                print("Error: Amount must be greater than 0")
                return False
            
            if not category.strip():
                print("Error: Category cannot be empty")
                return False
            
            if not description.strip():
                print("Error: Description cannot be empty")
                return False
            
            date = datetime.now().strftime("%Y-%m-%d")
            expense_id = self._get_next_id()
            
            with open(self.filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([expense_id, date, f"{amount:.2f}", category, description])
            
            print(f"\nExpense added successfully! (ID: {expense_id})")
            return True
            
        except ValueError:
            print("Error: Invalid amount. Please enter a valid number")
            return False
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def view_expenses(self):
        """Display all expenses"""
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                
                if len(rows) <= 1:
                    print("\nNo expenses recorded yet.")
                    return
                
                print("\n" + "="*80)
                print(f"{'ID':<5} {'Date':<12} {'Amount':<12} {'Category':<15} {'Description':<30}")
                print("="*80)
                
                for row in rows[1:]:
                    expense_id, date, amount, category, description = row
                    print(f"{expense_id:<5} {date:<12} ${amount:<11} {category:<15} {description:<30}")
                
                print("="*80)
                
        except FileNotFoundError:
            print("\nNo expenses file found. Start by adding an expense!")
        except Exception as e:
            print(f"Error viewing expenses: {e}")
    
    def delete_expense(self, expense_id):
        """Delete an expense by ID"""
        try:
            expense_id = int(expense_id)
            
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
            
            found = False
            new_rows = [rows[0]]
            
            for row in rows[1:]:
                if int(row[0]) == expense_id:
                    found = True
                    print(f"\nDeleted expense: ID {row[0]} - ${row[2]} - {row[3]} - {row[4]}")
                else:
                    new_rows.append(row)
            
            if not found:
                print(f"\nError: No expense found with ID {expense_id}")
                return False
            
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(new_rows)
            
            return True
            
        except ValueError:
            print("Error: Invalid ID. Please enter a valid number")
            return False
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False
    
    def calculate_total(self):
        """Calculate and display total expenses"""
        try:
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                
                total = 0.0
                count = 0
                
                for row in reader:
                    total += float(row[2])
                    count += 1
                
                if count == 0:
                    print("\nNo expenses to calculate.")
                    return
                
                print("\n" + "="*40)
                print("EXPENSE SUMMARY")
                print("="*40)
                print(f"Total Expenses: ${total:.2f}")
                print(f"Number of Expenses: {count}")
                print("="*40)
                
        except FileNotFoundError:
            print("\nNo expenses file found.")
        except Exception as e:
            print(f"Error calculating total: {e}")
    
    def show_categories(self):
        """Display available categories"""
        print("\nPredefined Categories:")
        for i, category in enumerate(self.predefined_categories, 1):
            print(f"  {i}. {category}")
        print(f"  {len(self.predefined_categories) + 1}. Custom (Enter your own)")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("         EXPENSE TRACKER")
    print("="*50)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Delete Expense")
    print("4. Calculate Total Expenses")
    print("5. Exit")
    print("="*50)


def main():
    """Main function"""
    tracker = ExpenseTracker()
    
    print("\nWelcome to Expense Tracker!")
    print("Track your daily expenses.")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n--- Add New Expense ---")
            tracker.show_categories()
            
            cat_choice = input("\nSelect category number: ").strip()
            try:
                cat_num = int(cat_choice)
                if 1 <= cat_num <= len(tracker.predefined_categories):
                    category = tracker.predefined_categories[cat_num - 1]
                elif cat_num == len(tracker.predefined_categories) + 1:
                    category = input("Enter custom category: ").strip()
                else:
                    print("Invalid category selection!")
                    continue
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue
            
            amount = input("Enter amount: $").strip()
            description = input("Enter description: ").strip()
            tracker.add_expense(amount, category, description)
        
        elif choice == "2":
            tracker.view_expenses()
        
        elif choice == "3":
            print("\n--- Delete Expense ---")
            tracker.view_expenses()
            
            if os.path.exists(tracker.filename):
                expense_id = input("\nEnter the ID of expense to delete (or 0 to cancel): ").strip()
                if expense_id != "0":
                    tracker.delete_expense(expense_id)
        
        elif choice == "4":
            tracker.calculate_total()
        
        elif choice == "5":
            print("\nThank you for using Expense Tracker!")
            print("Your expenses have been saved. Goodbye!")
            break
        
        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
