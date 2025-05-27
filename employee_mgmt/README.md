# Employee Management Django Project

This is a scaffold for the Employee Management system with:
- Custom user model (`CustomUser`)
- Employee CRUD operations
- CSV import/export without third-party packages
- Admin and Employee user roles
- Bootstrap-based styling

## Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install Django:
   ```bash
   pip install django
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

Enjoy!