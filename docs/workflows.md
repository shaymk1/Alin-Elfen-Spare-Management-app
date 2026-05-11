# Development Workflows

## Branching

- Use feature branches off `main` for work: `feature/<name>` or `fix/<name>`.
- Keep branches focused and open pull requests for review.

## Local Development

1. Create and activate a virtualenv:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app locally:

```powershell
python app.py
# open http://127.0.0.1:5000
```

## Testing

- Use `pytest` for unit tests. Run `pytest -q` locally and in CI.

## Linting & Formatting

- Optionally use `black` and `flake8` or similar tools to keep code consistent before PRs.

## Pull Requests

- Provide a clear summary, link any related issues, and list testing steps.
- Keep PRs small and focused for faster reviews.

## Release & Packaging

1. Ensure tests pass and the changelog is updated.
2. Build executable (Windows example):

```powershell
& .\venv\Scripts\Activate.ps1
pip install pyinstaller
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" app.py
```

3. Verify the generated executable in `dist/` on a clean Windows VM before distribution.

## CI Recommendations

- Run tests and linting on PRs.
- Optionally build artifacts (executables) in CI and attach them to releases.
