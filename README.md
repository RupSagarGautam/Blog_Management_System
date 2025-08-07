# Blog Management System

A comprehensive Django-based blog management system with admin approval workflow, category management, and user dashboard.

## Features

- **Blog Management**: Create, edit, delete, and view blog posts  
- **Admin Approval Workflow**: Blogs require admin approval before publication  
- **Category Management**: Organize blogs by categories  
- **Tag Support**: Add tags to blogs for better organization  
- **Media Support**: Upload images and attachments to blogs  
- **Dashboard**: View analytics and statistics  
- **Responsive Design**: Works on desktop and mobile devices  

## Requirements

- Python 3.8+
- Django 5.0+
- django-taggit
- pillow
- django-allauth
- requests
- PyJWT
- cryptography

## Installation

1. Clone the repository:
   git clone <repository-url>
   cd blog-management-system

2. Create a virtual environment and activate it:
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Run Migrations:
    python manage.py migrate

5. Create a superuser:
    python manage.py createsuperuser

6. Run the development Server:
    python manage.py runserver

7. Access The application at localhost:8000

## Usage
Admin Users
Log in to the admin panel at http://127.0.0.1:8000/admin/

Create categories for blogs

Approve, reject, or edit submitted blogs

View the dashboard for analytics

Regular Users
Browse blogs on the homepage

Create a new blog (requires login)

Edit or delete your own blogs

View blogs by category or tag

## License
This project is not licensed for commercial use.(Personal Use Only-For Educational Purporse)

## Acknowledgements
Django - The web framework used

Bootstrap - Frontend framework

django-taggit - For tagging functionality

[More About Project](https://github.com/Digital-Pathshala/Blog_Management_System.git)
