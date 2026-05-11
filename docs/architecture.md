# Architecture and Technology Choices

## Purpose

This document explains the rationale behind the chosen technology stack for the Spare Manager prototype and how the application is packaged for offline distribution as a single executable.

## Overview

- An offline desktop-oriented admin tool to manage spare parts, borrows and returns.
- Priorities: small footprint, simple distribution (single executable), minimal runtime dependencies, easy maintenance and quick development iteration.

## Language: Python

- Chosen for readability, rapid development, and a strong standard library. Python is well-suited for small utilities and admin tools.

## Web framework: Flask

- Lightweight, explicit, and minimal—Flask provides routing, request handling, and template rendering without imposing a heavy architecture.
- Server-side rendering keeps the frontend simple and eliminates the need for a JavaScript build step or complex client-side frameworks.

## Templates: Jinja2

- Server-side templating (the `templates/` folder) allows injecting data directly from the backend with simple logic in views.
- Keeps the front-end dependency surface minimal (no React/Vue build pipeline required).

## Database: SQLite

- Embedded, zero-configuration relational database stored as a single file. Ideal for offline desktop apps and small datasets.
- Easy to backup, copy, and bundle with a local executable.

## Frontend: HTML, CSS, Vanilla JavaScript

- A single stylesheet (`static/css/style.css`) and a small JS file (`static/js/app.js`) suffice for the UI behaviors and interactivity required.
- Avoiding a SPA framework (React/Vue/Angular) simplifies packaging and reduces binary size.

## Packaging: PyInstaller (single executable)

- Goal: produce a single runnable executable for target platforms (Windows .exe) so end users can run the app without installing Python or dependencies.
- PyInstaller usage notes:
  - Include application code (`app.py`), templates (`templates/`) and static assets (`static/`) as bundled data.
  - Example build command (Windows PowerShell):

```powershell
# Activate virtualenv
& .\venv\Scripts\Activate.ps1
# Install build deps if needed
pip install pyinstaller
# Build one-file executable (adjust paths/flags as needed)
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" app.py
```

  - After building, distribute the generated executable in `dist/` to users.
  - Signing the executable (optional) improves trust when distributing to Windows users.

## Virtual Environment & Dependencies

- Use `venv` to isolate dependencies during development. Keep `requirements.txt` up to date so the build environment is reproducible.

## Runtime & Deployment

- The app runs locally; no reverse proxy, HTTPS, or SSL termination is required because the intended distribution is an offline desktop executable.
- For local developer testing, run with the Flask dev server (as used during development). The packaged executable will embed the same app code.

## Security Considerations

- Since the app runs locally, network exposure is minimal; however:
  - Secure the machine running the executable (OS access controls, file permissions) because the SQLite file contains application data.
  - Consider code signing the produced executable for integrity and trust.
  - If you later expose the app over a network, revisit transport security (HTTPS) and authentication.

## Testing, Logging & Updates

- Keep automated tests for core logic where practical. Unit tests for business logic make refactors safer.
- Basic logging (to files) helps diagnose issues for local users.
- For updates, distribute new executables; consider a simple versioning scheme and a release channel (manual download or internal update script).

## Trade-offs and Alternatives

- Why not a SPA + API: A SPA adds build steps, a larger bundle, and more moving parts; for a small offline admin tool, server-rendered pages are simpler to package and maintain.
- Why not an embedded DB server: SQLite offers the lowest operational cost (no service to run). If scaling or concurrency becomes important, consider migrating to a client-server DB.

## Summary

This stack prioritizes simplicity, fast iteration, and easy distribution for an offline desktop tool. Packaging with PyInstaller produces a single executable that non-technical users can run with minimal setup while keeping development and maintenance straightforward.
