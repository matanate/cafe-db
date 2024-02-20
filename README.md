# Café Review Web App

## Overview

This is a Flask-based web application for reviewing and discovering cafes. Users can sign up, log in, add new cafes, and review existing ones. The app allows users to search for cafes by location or name and provides an option to view a random cafe.

## Getting Started

These instructions will help you set up and run the project on your local machine.

## Prerequisites

- Python 3.9
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Werkzeug

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cafe-review-web
```

2. Navigate to the project directory:

```bash
cd cafe-review-web
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables:

- DB_URI: Database connection URI.
- SECRET_KEY: Secret key for Flask.

4. Initialize the database:

```bash
flask db init
```

5. Apply migrations:

```bash
flask db upgrade
```

6. run python file:

```bash
python app.py
```

7. Open your web browser and navigate to http://127.0.0.1:5000/ to access the application.

## Features

- User Authentication: Users can sign up, log in, and log out. Passwords are securely hashed using the PBKDF2-SHA256 algorithm.

- Cafe Management: Users can add new cafes, review existing cafes, and search for cafes by location or name.

- Admin Privileges: Admins (user ID 1) have access to admin-only routes. Ordinary users can access regular features.
  .

- API Endpoints: The app provides API endpoints for retrieving information about all cafes, random cafe, searching cafes by location or name, and adding a new cafe.

## Usage

1. Open your web browser and navigate to http://127.0.0.1:5000/.

2. Sign up or log in to access the main features.

3. Explore cafes, add new cafes, and review existing ones.

4. Utilize the API endpoints for programmatic access to cafe information.

## Contributing

Feel free to contribute by opening issues or pull requests. Your feedback and contributions are welcome!

## Deployment (Live Demo)

Check out the live demo:
[Live Demo](https://cafe-db-web.onrender.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
