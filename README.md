# Personal Expense Tracker & Analyzer

A command-line application for tracking personal expenses with powerful analytics capabilities.

## Features

### Expense Management
- ✅ Add new expenses with date, amount, category, and payment method
- ✅ View all expenses
- ✅ Filter expenses by category
- ✅ Filter expenses by date range
- ✅ Delete expenses
- ✅ SQLite database for persistent storage

### Analytics Dashboard
- ✅ Overall spending summary
- ✅ Spending breakdown by category
- ✅ Category percentage analysis
- ✅ Payment method analysis
- ✅ Top 5 most expensive purchases
- ✅ Monthly spending trends
- ✅ Automated insights and pattern detection

## Technologies Used

- **Python 3** - Core programming language
- **SQLite3** - Database for data storage
- **Pandas** - Data analysis and manipulation
- **Data Engineering** - ETL pipeline (database → pandas → insights)
- **Data Analysis** - Statistical analysis and pattern recognition

## How to Run

python3 expense_tracker.py

## Structure

expense-tracker/
├── expense_tracker.py    # Main application
├── expenses.db          # SQLite database (created automatically)
├── README.md            # This file
└── DESIGN.md            # Project design document

## Code Architecture

### Expense Database Class
Handles all database operations:
∙ CRUD operations (Create, Read, Update, Delete)
∙ SQL queries
∙ Returns pandas DataFrames for analysis

### ExpenseAnalyzer Class
Performs data analysis using pandas:
∙ Aggregations and grouping
∙ Statistical calculations
∙ Pattern detection
∙ Trend analysis

### ExpenseTrackerUI Class
User interface and user experience:
∙ Interactive menu system
∙ Input validation
∙ Formatted output
∙ Error handling

### Sample Analytics
The dashboard provides insights such as:
∙ “Most frequent expense category: Food & Dining”
∙ “Highest spending category: Bills & Utilities ($200.00)”
∙ “Average daily spending: $35.67”
∙ Category breakdowns with percentages
∙ Payment method preferences

## Demonstrated

### Data Engineering
∙ Database design and schema creation
∙ SQL queries for data retrieval
∙ ETL pipeline (Extract from DB → Transform with pandas → Load insights)
∙ Data persistence and integrity

### Data Analysis
∙ Pandas DataFrames and Series
∙ GroupBy operations
∙ Aggregate functions (sum, mean, count, max, min)
∙ Time series analysis (monthly trends)
∙ Pattern recognition
∙ Statistical summaries

### Software Development
∙ Object-Oriented Programming
∙ Class design and encapsulation
∙ Input validation and error handling
∙ User interface design
∙ Code organization and documentation

### Future Enhancements
∙ Budget tracking and warnings
∙ Data visualization (charts and graphs)
∙ Export to CSV/Excel
∙ Recurring expense tracking
∙ Multi-user support
∙ Web interface
∙ Mobile app