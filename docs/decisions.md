# Architectural Decisions

This document captures high-level decisions made during the design and implementation of the Spare Manager prototype.

- Use Python as the primary language
	- Rationale: rapid development, readability, strong standard library, and broad ecosystem for packaging and scripting.

- Choose Flask as the web framework
	- Rationale: lightweight, explicit routing and templating with minimal ceremony. Server-side rendering (Jinja2) reduces frontend complexity and makes packaging simpler.

- Use SQLite for storage
	- Rationale: embedded single-file database provides portability and no operational overhead—ideal for offline desktop apps.

- Package as a single executable with PyInstaller
	- Rationale: end users should be able to run the app without installing Python or dependencies. PyInstaller bundles code, assets and interpreter into one file.

- Avoid SPA frameworks (React/Vue)
	- Rationale: SPA frameworks increase bundle size, require build tooling, and complicate packaging for a single-file offline executable. The app's UI needs are met with server-rendered templates and small JS.

- Keep UI styling custom and minimal
	- Rationale: a bespoke CSS file provides precise control over the look-and-feel with zero external UI framework dependencies.

- Prototype data models as dataclasses
	- Rationale: Python dataclasses are lightweight, typed, and easy to test; they suffice for the prototype without a full ORM.

- No external auth or SSO for initial release
	- Rationale: Offline distribution and single-machine usage reduce the need for complex authentication. Simple username/password or OS-level access control is sufficient initially.

These decisions prioritize simplicity, maintainability, and ease of distribution for end users.
