# Project Documentation: Tic Tac Toe

## Project Overview
This project is a web-based **Tic Tac Toe** application built with Django. It supports a tournament-style gameplay where two players can compete in multiple rounds. The application tracks scores, manages game states, and provides a detailed analytics dashboard for staff members to monitor overall performance and tournament history.

## Production Environment
The project is currently live and accessible at:
- **Production URL**: [https://tictactoe.idruiz.com](https://tictactoe.idruiz.com)

## Key Features
- **Tournament System**: Players can start a tournament by entering their names. The system tracks the overall score (wins for Player X, wins for Player O, and draws).
- **Interactive Gameplay**: A responsive board for local multiplayer (same screen).
- **Analytics Dashboard**: A restricted area (`/dashboard/`) for staff members that displays:
    - Total tournaments and matches played.
    - Global win rates for Player X and Player O.
    - Historical data of the last 10 tournaments.
- **Automated SSL**: Integrated with **Traefik** and **Let's Encrypt** for automatic HTTPS certificate management.

## Technical Stack
- **Backend**: Django 5.x
- **Database**: MariaDB 10.11
- **WSGI Server**: Gunicorn
- **Reverse Proxy**: Traefik v2.10
- **Containerization**: Docker & Docker Compose
- **Dependency Management**: Poetry

## Infrastructure & Deployment
The application is fully dockerized, consisting of three main services:
1.  **db**: MariaDB database for persistent storage of tournaments and matches.
2.  **web**: Django application served via Gunicorn.
3.  **traefik**: Edge router handling SSL termination and routing traffic to the web service.

### Environment Configuration
Critical settings are managed via environment variables defined in the `.env` file, including:
- `DJANGO_ALLOWED_HOSTS`: Set to `tictactoe.idruiz.com` for production.
- `DEBUG`: Set to `0` (False) in production.
- `DATABASE_URL` configurations (SQL_ENGINE, SQL_DATABASE, etc.).
- `TRAEFIK_CERT_EMAIL`: Used for Let's Encrypt registration.

## Data Model
- **Tournament**: Stores player names, cumulative scores, and timing information (`started_at`, `ended_at`).
- **Match**: Represents an individual round within a tournament, storing the board state (as a 9-character string) and the winner.

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
    DEBUG=0
    SECRET_KEY=your-secret-key
    DJANGO_ALLOWED_HOSTS=tictactoe.idruiz.com
    SQL_ENGINE=django.db.backends.mysql
    SQL_DATABASE=tictactoedb
    SQL_USER=phicus_admin
    SQL_PASSWORD=password
    SQL_HOST=db
    SQL_PORT=3306
    TRAEFIK_CERT_EMAIL=your-email@example.com
    ```

3.  **Run with Docker Compose**:
    ```bash
    docker-compose up -d --build
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
- **Play the Game**: Navigate to `https://tictactoe.idruiz.com` (or `http://localhost` if running locally) to start a new tournament.
- **View Dashboard**: Access the analytics at `/dashboard/`. You will be prompted to log in with your superuser credentials.
- **Admin Interface**: Manage data directly at `/admin/`.

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

## Contact & Maintenance
For maintenance or updates, ensure that the `.env` file is properly configured and the Docker services are running:
```bash
docker-compose up -d
```

## License
This project is licensed under the GNU General Public License v3.0
