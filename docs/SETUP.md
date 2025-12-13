## App Setup Guide

### Requirements

- **Python 3.12+**
- **uv** (fast Python package installer and resolver)
- **Docker** (installed & running)
- **PostgreSQL** (client, CLI, or pgAdmin recommended)
- **Make** (for running Makefile commands)

---

### Setup Steps

1. **Clone the Repository**

```bash
  git clone [https://github.com/heisdanielade/api-smart-savings.git](https://github.com/ArtemRuzhevych/nlp-savebuddy.git)
  cd nlp-savebuddy
```

2. **Install Dependencies**

This project uses `uv` for dependency management.
First, ensure `uv` is installed globally:

```bash
  pip install uv
```
Then, sync the project environment to install the exact versions of dependencies:
```bash
  uv sync
```

3. **Configure Environment Variables**

- Copy `.env.example` → `.env` (created by you)
- Create a PostgreSQL database (e.g., `savebuddy`)
- Update `.env` with your **database credentials**
- Update other values as provided privately by the project manager: ([@heisdanielade](https://github.com/heisdanielade))

4. **Run App Commands**

```bash
make build      # Start app using Docker
make down       # Stop app
make tests      # Run tests
```

More helpful commands are provided in `Makefile` in the project's root directory.

5. **Verification**
   Once the app starts, verify it’s running by visiting:
   **_http://localhost:2084_**