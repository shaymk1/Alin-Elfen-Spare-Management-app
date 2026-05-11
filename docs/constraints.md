# Project Constraints

- Offline-first: the application must run entirely locally without requiring network connectivity.
- Single-executable distribution: the deliverable should be an install-free executable (e.g., built with PyInstaller) so end users do not need to install Python or dependencies.
- Small footprint: minimize binary size and runtime dependencies to simplify distribution and execution on client machines.
- Zero or minimal external services: avoid relying on external APIs, SaaS or cloud infrastructure.
- Embedded storage: use a single-file embedded datastore (SQLite) for simplicity and portability.
- Limited concurrency requirements: designed primarily for single-user or small-team offline use; high-concurrency server-grade scaling is out of scope for this phase.
- Cross-platform packaging (future): primary target is Windows executable, with potential future support for macOS/Linux.

These constraints guided architecture and technology decisions: prefer server-side rendering, avoid heavy frontend frameworks, and bundle static assets into the executable.
