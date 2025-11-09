## Repo snapshot

This is a tiny, single-script Python project that calculates a monthly budget and a 12-month savings projection.

- Key file: `budget.py` — the entire app lives here. Read `compute_report()` for the core logic and `print_report()` for output formatting.
- Doc: `README.md` contains the quick-start run command and an example input JSON.

## How to run (developer workflow)

- Run the sample report from the repo root (Windows PowerShell):

```powershell
python "C:\Users\Public\money_task\budget.py"
```

- To run with a custom JSON input use `-i` or `--input`:

```powershell
python budget.py -i my_input.json
```

There is no build step or external runtime dependency beyond the Python standard library (Decimal is used). Target Python 3.

## Important patterns & conventions (project-specific)

- Monetary values in runtime and in JSON are strings (e.g. "4000"). The code uses a helper D(value) to convert to a Decimal and quantize to 2 decimal places. Prefer passing string literals when creating or editing sample JSON in the repo.

- Input JSON shape (example fields used by `compute_report`):

```json
{
  "currency": "USD",
  "monthly_income": "4000",
  "expenses": { "rent": "1200", "groceries": "400" },
  "monthly_savings_goal": "500"
}
```

- `compute_report(data: dict)` returns a dictionary with these important keys:
  - `income`, `expenses` (dict of categories -> Decimal), `total_expenses`, `disposable`,
  - `monthly_savings_goal`, `monthly_savings`, `surplus_after_savings`,
  - `projection_12m` — list of objects `{month: int, balance: Decimal}`.

## Editing guidance for AI agents

- Small, local edits are preferred. `budget.py` is small; change behavior in-place and run the script to validate.
- Preserve the `D()` helper semantics: always convert external input to Decimal via `D()` and keep `.quantize(Decimal('0.01'))` rounding.
- When adding or editing JSON examples, use string values for amounts (not numbers) — this matches how the script reads the input.

## Tests / CI

- There are currently no tests or CI files. After making functional changes, validate by running the script with the sample input and one custom JSON file that includes an edge case (zero income, large expenses, missing fields).

## Common small tasks & examples

- Add a new expense category: modify the SAMPLE dict in `budget.py` and run the script to confirm output formatting unchanged.
- Add an output CSV exporter: implement a new function that reads `report = compute_report(data)` and writes `projection_12m` rows; keep Decimal values stringified with two decimals.

## Files to reference

- `budget.py` — main logic and CLI handling.
- `README.md` — run instructions and example JSON.

If any of this is unclear or you'd like a different level of detail (e.g., example tests, suggested unit-test harness, or a CLI argparser), tell me which part to expand and I will update this file.
