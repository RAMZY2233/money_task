# Simple Monthly Budget Tool

This small Python script prints a monthly budget breakdown, planned savings, and a 12-month savings projection.

Quick start

1. Ensure Python 3 is installed and on PATH.
2. Run the script (Windows PowerShell):

```powershell
python "C:\Users\Public\money_task\budget.py"
```

Optional: supply a JSON input file with `-i`/`--input`.

Example input JSON structure:

```json
{
  "currency": "USD",
  "monthly_income": "4000",
  "expenses": {"rent":"1200", "groceries":"400"},
  "monthly_savings_goal": "500"
}
```

The script uses Decimal arithmetic for money values.
