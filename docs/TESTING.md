# Testing

This project currently contains core application logic in `app.py` that can be covered by unit tests.

Recommendations:

- Use `pytest` for unit tests. Create a `tests/` folder and name test files `test_*.py`.
- Install testing deps in your venv:

```powershell
pip install pytest
```

- Run tests:

```powershell
pytest -q
```

- Add CI later to run tests automatically on PRs.

If you want, I can scaffold a minimal `tests/` folder and a couple of example tests for the dataclasses and stats calculations.