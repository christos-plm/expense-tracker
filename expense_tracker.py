# expense_tracker.py - Personal Expense Tracker with Analysis
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# ===== DATABASE SETUP =====

class ExpenseDatabase:
    """Handles all database operations for expenses"""
    
    def __init__(self, db_name='expenses.db'):
        self.db_name = db_name
        self._init_database()
    
    def _init_database(self):
        """Create the expenses table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                payment_method TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ Database initialized")
    
    def add_expense(self, date, amount, category, description, payment_method):
        """Add a new expense to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (date, amount, category, description, payment_method)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, category, description, payment_method))
        
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return expense_id
    
    def get_all_expenses(self):
        """Retrieve all expenses as a pandas DataFrame"""
        conn = sqlite3.connect(self.db_name)
        
        # Load directly into pandas
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
        
        conn.close()
        return df
    
    def get_expenses_by_date_range(self, start_date, end_date):
        """Get expenses within a date range"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT * FROM expenses 
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        
        conn.close()
        return df
    
    def get_expenses_by_category(self, category):
        """Get all expenses in a specific category"""
        conn = sqlite3.connect(self.db_name)
        
        query = "SELECT * FROM expenses WHERE category = ? ORDER BY date DESC"
        df = pd.read_sql_query(query, conn, params=(category,))
        
        conn.close()
        return df
    
    def delete_expense(self, expense_id):
        """Delete an expense by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_expense_count(self):
        """Get total number of expenses"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM expenses")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count


# ===== ANALYSIS LAYER =====

class ExpenseAnalyzer:
    """Analyzes expenses using pandas for insights"""
    
    def __init__(self, database):
        self.db = database
    
    def get_spending_summary(self):
        """Get overall spending summary"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return None
        
        summary = {
            'total_expenses': len(df),
            'total_spent': df['amount'].sum(),
            'average_expense': df['amount'].mean(),
            'largest_expense': df['amount'].max(),
            'smallest_expense': df['amount'].min(),
        }
        
        return summary
    
    def spending_by_category(self):
        """Analyze spending by category"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return None
        
        category_summary = df.groupby('category').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        category_summary.columns = ['Total', 'Count', 'Average']
        category_summary = category_summary.sort_values('Total', ascending=False)
        
        return category_summary
    
    def spending_by_payment_method(self):
        """Analyze spending by payment method"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return None
        
        payment_summary = df.groupby('payment_method').agg({
            'amount': ['sum', 'count']
        }).round(2)
        
        payment_summary.columns = ['Total', 'Count']
        payment_summary = payment_summary.sort_values('Total', ascending=False)
        
        return payment_summary
    
    def monthly_spending_trend(self):
        """Analyze spending trends by month"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return None
        
        # Convert date to datetime and extract month
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        monthly = df.groupby('month').agg({
            'amount': ['sum', 'count', 'mean']
        }).round(2)
        
        monthly.columns = ['Total Spent', 'Num Expenses', 'Avg Expense']
        
        return monthly
    
    def top_expenses(self, n=5):
        """Get the top N most expensive purchases"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return None
        
        return df.nlargest(n, 'amount')[['date', 'amount', 'category', 'description']]
    
    def category_percentage(self):
        """Calculate what percentage of total spending each category represents"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return None
        
        total_spending = df['amount'].sum()
        
        category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        category_pct = (category_totals / total_spending * 100).round(2)
        
        result = pd.DataFrame({
            'Amount': category_totals,
            'Percentage': category_pct
        })
        
        return result
    
    def find_patterns(self):
        """Identify spending patterns and insights"""
        df = self.db.get_all_expenses()
        
        if df.empty:
            return []
        
        patterns = []
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date'])
        
        # Pattern 1: Most frequent category
        most_frequent_category = df['category'].value_counts().index[0]
        patterns.append(f"Most frequent expense category: {most_frequent_category}")
        
        # Pattern 2: Highest spending category
        highest_spending_cat = df.groupby('category')['amount'].sum().idxmax()
        highest_amount = df.groupby('category')['amount'].sum().max()
        patterns.append(f"Highest spending category: {highest_spending_cat} (${highest_amount:.2f})")
        
        # Pattern 3: Preferred payment method
        preferred_payment = df['payment_method'].value_counts().index[0]
        patterns.append(f"Most used payment method: {preferred_payment}")
        
        # Pattern 4: Average daily spending
        date_range = (df['date'].max() - df['date'].min()).days + 1
        daily_avg = df['amount'].sum() / date_range
        patterns.append(f"Average daily spending: ${daily_avg:.2f}")
        
        # Pattern 5: Large purchases (above average)
        avg_expense = df['amount'].mean()
        large_purchases = len(df[df['amount'] > avg_expense * 2])
        patterns.append(f"Large purchases (>2x average): {large_purchases}")
        
        return patterns


# ===== USER INTERFACE =====

class ExpenseTrackerUI:
    """Command-line user interface for the expense tracker"""
    
    CATEGORIES = [
        'Food & Dining',
        'Transportation',
        'Shopping',
        'Entertainment',
        'Bills & Utilities',
        'Healthcare',
        'Other'
    ]
    
    PAYMENT_METHODS = [
        'Cash',
        'Credit Card',
        'Debit Card',
        'Digital Wallet'
    ]
    
    def __init__(self):
        self.db = ExpenseDatabase()
        self.analyzer = ExpenseAnalyzer(self.db)
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 70)
        print("                    EXPENSE TRACKER")
        print("=" * 70)
        
        # Show quick stats
        count = self.db.get_expense_count()
        print(f"Total expenses tracked: {count}")
        
        if count > 0:
            summary = self.analyzer.get_spending_summary()
            print(f"Total spent: ${summary['total_spent']:.2f}")
        
        print("=" * 70)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. View Expenses by Date Range")
        print("5. Delete Expense")
        print("6. Analysis Dashboard")
        print("7. Exit")
        print("=" * 70)
    
    def get_valid_number(self, prompt, min_val=None, max_val=None):
        """Get a valid number from user with validation"""
        while True:
            try:
                value = float(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"❌ Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_date(self):
        """Get a date from user with validation"""
        while True:
            date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            
            if not date_str:
                return datetime.now().strftime('%Y-%m-%d')
            
            try:
                # Validate date format
                datetime.strptime(date_str, '%Y-%m-%d')
                return date_str
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD")
    
    def select_from_list(self, items, prompt):
        """Display a list and let user select one"""
        print(f"\n{prompt}")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
        
        while True:
            try:
                choice = int(input("\nSelect number: "))
                if 1 <= choice <= len(items):
                    return items[choice - 1]
                print(f"❌ Please select a number between 1 and {len(items)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def add_expense(self):
        """Add a new expense"""
        print("\n" + "=" * 70)
        print("ADD NEW EXPENSE")
        print("=" * 70)
        
        # Get expense details
        date = self.get_date()
        amount = self.get_valid_number("Enter amount: $", min_val=0.01)
        category = self.select_from_list(self.CATEGORIES, "Select category:")
        description = input("Enter description: ").strip()
        payment_method = self.select_from_list(self.PAYMENT_METHODS, "Select payment method:")
        
        # Confirm before adding
        print("\n" + "-" * 70)
        print("Review your expense:")
        print(f"  Date: {date}")
        print(f"  Amount: ${amount:.2f}")
        print(f"  Category: {category}")
        print(f"  Description: {description}")
        print(f"  Payment: {payment_method}")
        print("-" * 70)
        
        confirm = input("\nAdd this expense? (y/n): ").lower()
        
        if confirm == 'y':
            expense_id = self.db.add_expense(date, amount, category, description, payment_method)
            print(f"✓ Expense #{expense_id} added successfully!")
        else:
            print("❌ Expense not added")
    
    def view_all_expenses(self):
        """Display all expenses"""
        print("\n" + "=" * 70)
        print("ALL EXPENSES")
        print("=" * 70)
        
        df = self.db.get_all_expenses()
        
        if df.empty:
            print("No expenses found. Add some expenses to get started!")
            return
        
        # Format for display
        df['amount'] = df['amount'].apply(lambda x: f"${x:.2f}")
        
        print(df.to_string(index=False))
        print(f"\nTotal expenses: {len(df)}")
    
    def view_by_category(self):
        """View expenses filtered by category"""
        print("\n" + "=" * 70)
        print("VIEW BY CATEGORY")
        print("=" * 70)
        
        category = self.select_from_list(self.CATEGORIES, "Select category:")
        
        df = self.db.get_expenses_by_category(category)
        
        if df.empty:
            print(f"\nNo expenses found in category: {category}")
            return
        
        print(f"\n{category} Expenses:")
        print("-" * 70)
        
        df['amount'] = df['amount'].apply(lambda x: f"${x:.2f}")
        print(df[['date', 'amount', 'description', 'payment_method']].to_string(index=False))
        
        total = self.db.get_expenses_by_category(category)['amount'].sum()
        print(f"\nTotal in {category}: ${total:.2f}")
    
    def view_by_date_range(self):
        """View expenses in a date range"""
        print("\n" + "=" * 70)
        print("VIEW BY DATE RANGE")
        print("=" * 70)
        
        print("\nStart date:")
        start_date = self.get_date()
        
        print("\nEnd date:")
        end_date = self.get_date()
        
        df = self.db.get_expenses_by_date_range(start_date, end_date)
        
        if df.empty:
            print(f"\nNo expenses found between {start_date} and {end_date}")
            return
        
        print(f"\nExpenses from {start_date} to {end_date}:")
        print("-" * 70)
        
        df['amount'] = df['amount'].apply(lambda x: f"${x:.2f}")
        print(df[['date', 'amount', 'category', 'description']].to_string(index=False))
        
        total = self.db.get_expenses_by_date_range(start_date, end_date)['amount'].sum()
        print(f"\nTotal in date range: ${total:.2f}")
    
    def delete_expense(self):
        """Delete an expense"""
        print("\n" + "=" * 70)
        print("DELETE EXPENSE")
        print("=" * 70)
        
        # Show recent expenses
        df = self.db.get_all_expenses()
        
        if df.empty:
            print("No expenses to delete!")
            return
        
        print("\nRecent expenses:")
        recent = df.head(10)
        print(recent[['id', 'date', 'amount', 'category', 'description']].to_string(index=False))
        
        try:
            expense_id = int(input("\nEnter expense ID to delete (0 to cancel): "))
            
            if expense_id == 0:
                print("❌ Deletion cancelled")
                return
            
            # Get the expense details before deleting
            expense = df[df['id'] == expense_id]
            
            if expense.empty:
                print(f"❌ No expense found with ID {expense_id}")
                return
            
            # Show what will be deleted
            print("\nExpense to delete:")
            print(f"  Date: {expense.iloc[0]['date']}")
            print(f"  Amount: ${expense.iloc[0]['amount']:.2f}")
            print(f"  Category: {expense.iloc[0]['category']}")
            print(f"  Description: {expense.iloc[0]['description']}")
            
            confirm = input("\nAre you sure? (y/n): ").lower()
            
            if confirm == 'y':
                if self.db.delete_expense(expense_id):
                    print(f"✓ Expense #{expense_id} deleted successfully!")
                else:
                    print(f"❌ Failed to delete expense")
            else:
                print("❌ Deletion cancelled")
                
        except ValueError:
            print("❌ Invalid expense ID")
    
    def show_dashboard(self):
        """Display the analysis dashboard"""
        print("\n" + "=" * 70)
        print("                   ANALYSIS DASHBOARD")
        print("=" * 70)
        
        # Check if there are any expenses
        if self.db.get_expense_count() == 0:
            print("\nNo expenses to analyze yet. Add some expenses first!")
            return
        
        # 1. Overall Summary
        print("\n1. OVERALL SUMMARY:")
        print("-" * 70)
        summary = self.analyzer.get_spending_summary()
        print(f"Total Expenses: {summary['total_expenses']}")
        print(f"Total Spent: ${summary['total_spent']:.2f}")
        print(f"Average Expense: ${summary['average_expense']:.2f}")
        print(f"Largest Expense: ${summary['largest_expense']:.2f}")
        print(f"Smallest Expense: ${summary['smallest_expense']:.2f}")
        
        # 2. Spending by Category
        print("\n2. SPENDING BY CATEGORY:")
        print("-" * 70)
        category_summary = self.analyzer.spending_by_category()
        print(category_summary)
        
        # 3. Category Percentages
        print("\n3. SPENDING BREAKDOWN (%):")
        print("-" * 70)
        category_pct = self.analyzer.category_percentage()
        print(category_pct)
        
        # 4. Payment Methods
        print("\n4. PAYMENT METHOD BREAKDOWN:")
        print("-" * 70)
        payment_summary = self.analyzer.spending_by_payment_method()
        print(payment_summary)
        
        # 5. Top Expenses
        print("\n5. TOP 5 MOST EXPENSIVE PURCHASES:")
        print("-" * 70)
        top = self.analyzer.top_expenses(5)
        print(top.to_string(index=False))
        
        # 6. Monthly Trend
        print("\n6. MONTHLY SPENDING TREND:")
        print("-" * 70)
        monthly = self.analyzer.monthly_spending_trend()
        if monthly is not None and not monthly.empty:
            print(monthly)
        else:
            print("Need more than one month of data to show trends")
        
        # 7. Spending Patterns
        print("\n7. SPENDING PATTERNS & INSIGHTS:")
        print("-" * 70)
        patterns = self.analyzer.find_patterns()
        for i, pattern in enumerate(patterns, 1):
            print(f"  • {pattern}")
        
        print("\n" + "=" * 70)
    
    def run(self):
        """Main application loop"""
        print("\n" + "=" * 70)
        print("        WELCOME TO EXPENSE TRACKER")
        print("=" * 70)
        print("\nTrack your expenses and gain insights into your spending habits!")
        
        while True:
            self.display_menu()
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_all_expenses()
            elif choice == '3':
                self.view_by_category()
            elif choice == '4':
                self.view_by_date_range()
            elif choice == '5':
                self.delete_expense()
            elif choice == '6':
                self.show_dashboard()
            elif choice == '7':
                print("\n" + "=" * 70)
                print("Thank you for using Expense Tracker!")
                print("Your data has been saved.")
                print("=" * 70)
                break
            else:
                print("❌ Invalid option. Please select 1-7.")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")


# ===== MAIN PROGRAM =====

def main():
    """Run the expense tracker application"""
    app = ExpenseTrackerUI()
    app.run()


if __name__ == "__main__":
    # Comment out the test code and run the actual app
    main()


# ===== TEST ANALYSIS =====
#
# if __name__ == "__main__":
#    print("=" * 70)
#    print("EXPENSE TRACKER - ANALYSIS TEST")
#    print("=" * 70)
#
#    # Create database and analyzer
#    db = ExpenseDatabase()
#    analyzer = ExpenseAnalyzer(db)
#
#    # Overall summary
#    print("\n1. OVERALL SPENDING SUMMARY:")
#    print("-" * 70)
#    summary = analyzer.get_spending_summary()
#    if summary:
#        print(f"Total expenses: {summary['total_expenses']}")
#        print(f"Total spent: ${summary['total_spent']:.2f}")
#        print(f"Average expense: ${summary['average_expense']:.2f}")
#        print(f"Largest expense: ${summary['largest_expense']:.2f}")
#        print(f"Smallest expense: ${summary['smallest_expense']:.2f}")
#
#    # Spending by category
#    print("\n2. SPENDING BY CATEGORY:")
#    print("-" * 70)
#    category_summary = analyzer.spending_by_category()
#    if category_summary is not None:
#        print(category_summary)
#
#    # Category percentages
#    print("\n3. CATEGORY BREAKDOWN (%):")
#    print("-" * 70)
#    category_pct = analyzer.category_percentage()
#    if category_pct is not None:
#        print(category_pct)
#
#    # Payment methods
#    print("\n4. SPENDING BY PAYMENT METHOD:")
#    print("-" * 70)
#    payment_summary = analyzer.spending_by_payment_method()
#    if payment_summary is not None:
#        print(payment_summary)
#
#    # Top expenses
#    print("\n5. TOP 5 MOST EXPENSIVE PURCHASES:")
#    print("-" * 70)
#    top = analyzer.top_expenses(5)
#    if top is not None:
#        print(top.to_string(index=False))
#
#    # Spending patterns
#    print("\n6. SPENDING PATTERNS & INSIGHTS:")
#    print("-" * 70)
#    patterns = analyzer.find_patterns()
#    for i, pattern in enumerate(patterns, 1):
#        print(f"{i}. {pattern}")
#
#    print("\n" + "=" * 70)
#    print("ANALYSIS TEST COMPLETE!")
#    print("=" * 70)

