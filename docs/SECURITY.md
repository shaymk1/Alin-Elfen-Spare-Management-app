# Security

This application is intended to run locally as an offline executable. Security considerations focus on protecting local data and ensuring safe distribution.

- The SQLite database file contains application data; protect it with OS-level permissions.
- Consider code signing the executable for Windows distributions to help users trust the binary.
- Do not expose the application to untrusted networks without adding transport encryption (HTTPS) and authentication.
- If you accept user credentials, never store plaintext passwords; use secure password hashing.

Reporting a vulnerability

If you discover a security issue, please contact the project maintainer and include steps to reproduce, affected versions, and suggested mitigations.