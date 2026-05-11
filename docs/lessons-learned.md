# Lessons Learned

1. Keep the UI simple for desktop/offline apps
	- Server-side rendering and minimal JavaScript reduce packaging complexity and make the app easier to test and bundle.

2. Bundle static assets intentionally
	- PyInstaller requires explicit inclusion of templates and static files. Missing assets are a common packaging pitfall; verify the built executable on a clean environment.

3. Prefer small, well-scoped datamodels early
	- Dataclasses provide a lightweight way to represent domain objects without an ORM; they speed up prototypes and keep the codebase approachable.

4. Design for single-user first
	- Building for offline/single-machine use simplified the architecture, but synchronization and concurrency become non-trivial if multi-user support is added later.

5. CSS-first layouts are easier to iterate
	- A single stylesheet with CSS variables made theme adjustments and layout updates straightforward.

6. Keep packaging and build steps documented
	- Clear build instructions (see `docs/SETUP.md`) reduce friction when producing releases or debugging user-reported issues.

