# Phicus Project - Tic Tac Toe

A Django-based Tic Tac Toe application that supports tournaments between two players, round tracking, and a metrics dashboard for tournament analytics.

## Features

- **Tournament System**: Start a tournament between two players and play multiple rounds.
- **Interactive Board**: A responsive Tic Tac Toe board for local multiplayer.
- **Analytics Dashboard**: A staff-only dashboard to view global statistics, including:
  - Total tournaments and matches played.
  - Total wins for Player X and Player O.
  - Draw counts and win rates.
  - Recent tournament history.
- **Dockerized Environment**: Ready for development and production using Docker and Docker Compose.
- **HTTPS Ready**: Configured with Traefik and Let's Encrypt for automatic SSL certificates.

## Project Structure

- `config/`: Django project configuration (settings, URLs, WSGI/ASGI).
- `tic_tac_toe/`: Main application logic.
  - `models.py`: Database schema for `Tournament` and `Match`.
  - `views.py`: Logic for game flow and analytics.
  - `templates/`: HTML templates for the game and dashboard.
- `Dockerfile` & `compose.yml`: Containerization settings.
- `pyproject.toml` & `poetry.lock`: Dependency management with Poetry.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/) (optional, for local development without Docker)

### Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd phicus_project
    ```

2.  **Configure environment variables**:
    Create a `.env` file in the root directory and configure the following variables (refer to `compose.yml` and `config/settings.py`):
    ```env
    DEBUG=False
    SECRET_KEY=your-secret-key
    DJANGO_ALLOWED_HOSTS=localhost
    SQL_ENGINE=django.db.backends.mysql
    SQL_DATABASE=phicus_db
    SQL_USER=user
    SQL_PASSWORD=password
    SQL_HOST=db
    SQL_PORT=3306
    TRAEFIK_CERT_EMAIL=your-email@example.com
    ```

3.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This will start the MariaDB database, the Django web application (via Gunicorn), and the Traefik reverse proxy.

4.  **Run Migrations**:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Create a Superuser** (to access the dashboard):
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

### Usage

- **Play the Game**: Navigate to `http://localhost` (or your configured host) to start a new tournament.
- **View Dashboard**: Access the analytics at `http://localhost/dashboard/`. You will be prompted to log in with your superuser credentials.
- **Admin Interface**: Manage data directly at `http://localhost/admin/`.

## Development

To run the project locally without Docker:

1.  Install dependencies:
    ```bash
    poetry install
    ```
2.  Run migrations (ensure you have a local database configured or use SQLite by default):
    ```bash
    poetry run python manage.py migrate
    ```
3.  Start the development server:
    ```bash
    poetry run python manage.py runserver
    ```

## License

This project is licensed under the GNU General Public License v3.0
