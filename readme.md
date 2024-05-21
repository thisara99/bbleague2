
# Basket League Project

[![Django](https://img.shields.io/badge/Django-3.2.3-green.svg)](https://www.djangoproject.com/)

## Basketball League Management System
Overview

This project is a REST API developed for a basketball league to manage and monitor games and rankings for a tournament. The system tracks the progress of games, teams, and individual players, providing comprehensive insights into the tournament's outcomes and player performances.
Tournament Structure

    Qualifying Rounds: A total of 16 teams participated in the first qualifying round. 8 teams advanced to the next round, continuing until one team was crowned champion.
    Teams: Each team comprises a coach and 10 players, although not all players participate in every game.

User Roles and Capabilities

The system supports three types of users, each with distinct capabilities:

    League Admin
        View All Teams: Access details of all teams, including average scores and player lists.
        View Player Details: See individual player information such as name, height, average score.
        Site Usage Statistics: Monitor site usage statistics, including:

    Coach
        Team Management: Select their team to view the list of players and the team's average score.
        Player Details: Access personal details of selected players, including name, height, average score.
        Filter Players: Filter players to display only those with average scores in the 90th percentile within the team.

    Player
        View Scoreboard: Access the scoreboard to see all games and final scores, along with the competition's progress and the winning team.

System Features

    Authentication: All users (admin, coach, player) can log in and log out of the system.
    Scoreboard: Displays all games, final scores, and the progression of the competition, indicating the winning team.
    Team and Player Insights: Detailed views and filters for coaches and admins to manage and analyze team and player performance.

This REST API provides a robust solution for managing a basketball tournament, ensuring that all relevant statistics and information are easily accessible to the league's admin, coaches, and players.

## Features

- User authentication (sign up, login, logout)
- RESTful API with Django REST Framework
- Admin interface for managing users

## Installation

### Prerequisites

- Python 3.x
- Django 3.x
- SQLite for development

### Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/thisara99/bbleague2.git
   cd bbleague
### Create and activate a virtual environment:

On Windows:

    python -m venv venv
    .\venv\Scripts\activate

On macOS and Linux:

    python3 -m venv venv
    source venv/bin/activate

### Install the dependencies:

    pip install -r requirements.txt

### Set up the database:

    python manage.py makemigrations 
    python manage.py migrate 

### reate a superuser :

    python manage.py createsuperuser


### Run the development server:

    python manage.py runserver

## Usage

    Running the Application
### To start the development server, run:

    python manage.py runserver

### Accessing the Application
Open your web browser and go to http://127.0.0.1:8000/.

### swagger:

      http://localhost:8000/swagger/


### Contact
Thisara De Silva - thisarais@gmail.com
