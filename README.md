# Thread Clone

**Thread Clone** is a social media thread clone project built using [Django](https://www.djangoproject.com/) and [HTMX](https://htmx.org/), allowing users to create and participate in threaded discussions. This README provides an overview of the project and instructions for getting started.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with **Thread Clone**, follow these instructions:

### Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- Python (version 3.10.12) or higher

You can install Python from the [official Python website](https://www.python.org/downloads/).

### Installation

1. Clone the Thread Clone repository to your local machine:

```bash
git clone https://github.com/ahnge/thread-clone.git
```

2. Navigate to the project directory:

```bash
cd thread-clone
```

3. Set up a virtual environment (recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

On windows:

```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

5. Install project dependencies:

```bash
pip install -r requirements.txt
```

6. Apply database migrations:

```bash
python manage.py migrate
```

7. Create a superuser account for admin access:

```bash
python manage.py createsuperuser
```

8. Start the development server:

```bash
python manage.py runserver
```

The Thread Clone should now be running at http://localhost:8000/. You can access the admin interface at http://localhost:8000/admin/ to manage threads and users.

## Usage

With **Thread Clone**, users can:

- Create and participate in threaded discussions.
- Reply to existing threads and comments.
- Like and repost threads and comments
- Follow users
- Manage their user profiles.
- To see the project in action, visit the development server URL and start exploring.

## Contributing

We welcome contributions. To contribute:

- Fork the repository on GitHub.
- Create a branch for your feature or bug fix.
- Make your changes and commit them with descriptive messages.
- Push your branch to your fork.
- Open a pull request with details about your changes.

## License

This project is licensed under the GNU General Public License, Version 3 (GPLv3) - see the [LICENSE](LICENSE.txt) file for details.
