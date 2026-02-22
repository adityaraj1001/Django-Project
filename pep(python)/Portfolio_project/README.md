Aditya Raj — Full Stack Portfolio
This is a production-style Django application showcasing a complete portfolio with a professional frontend, REST API, and automated DevOps pipeline.
Key Features:
Public Portfolio: Responsive Home, About, and Projects pages with slug-based routing .
Auth System: Secure signup, login, and admin-protected dashboard access .
Contact Workflows: Database storage for messages with automated admin notifications and user confirmations .
REST API: Data endpoints for projects and contacts powered by Django REST Framework .
DevOps Ready: Containerized architecture using Docker with PostgreSQL integration .
CI/CD Pipeline: Automated testing and build verification via GitHub Actions .
Setup InstructionsLocal Development (Manual)Install Dependencies:Bashpip install -r requirements.txt
Database: Configure your PostgreSQL credentials in your environment variables or settings.py.Migrate: Setup your database tables.+1Bashpython manage.py migrate
Admin User: Create an account for the dashboard and admin panel.
Bashpython manage.py createsuperuser
Run:Bashpython manage.py runserver
Docker Setup (Recommended)Deploy the entire stack (Django + PostgreSQL) with a single command:Bashdocker-compose up --build

DevOps & EngineeringPostgreSQL:
Used as the primary production-style database.
GitHub Actions: Pipeline automatically runs tests and verifies Docker builds on every push .Security: Support for environment variables for secure sensitive configurations