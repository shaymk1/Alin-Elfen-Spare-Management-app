# Setup & Build (Development and Packaging)

## Development setup

1. Create and activate a Python virtual environment:

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
# then open http://127.0.0.1:5000
```

## Packaging for distribution (single executable)

This project is intended to be distributed as an offline executable. A common tool is PyInstaller.

Example (Windows PowerShell):

```powershell
# Activate virtualenv
& .\venv\Scripts\Activate.ps1
# Install PyInstaller if not present
pip install pyinstaller
# Build single-file executable and bundle templates/static
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" app.py
```

After the build, the produced executable will be in `dist/`.

Notes:
- Include any runtime data files alongside the executable if your build flags differ.
- Test the produced executable on a clean environment to ensure all data is bundled correctly.