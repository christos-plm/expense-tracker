# Expense Tracker - Project Design

## Database Schema

### expenses table
- id (INTEGER PRIMARY KEY)
- date (TEXT) - Date of expense
- amount (REAL) - Amount spent
- category (TEXT) - Category (Food, Transport, Entertainment, etc.)
- description (TEXT) - Short description
- payment_method (TEXT) - Cash, Credit Card, Debit Card

## Features

### Basic (Must Have)
- [x] Add new expense
- [x] View all expenses
- [x] View expenses by date range
- [x] Delete expense
- [x] SQLite database storage

### Analysis (Core Value)
- [x] Total spending by category
- [x] Monthly spending trends
- [x] Average expense per category
- [x] Most expensive purchases
- [x] Payment method breakdown
- [x] Identify spending patterns

### Advanced (Nice to Have)
- [ ] Budget warnings
- [ ] Export to CSV
- [ ] Visualizations
- [ ] Recurring expenses

## User Flow

1. Main menu with options
2. Add expense: prompt for date, amount, category, description
3. View expenses: show all or filter by date/category
4. Analyze: show insights and patterns
5. Exit

## Categories

- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Other

## Success Criteria

- Can add and store expenses
- Can retrieve and display expenses
- Provides meaningful spending insights
- Data persists between sessions
- Clean, user-friendly interface
