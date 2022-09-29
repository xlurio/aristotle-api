<h1 align="center">AristotleAPI</h1>
<p align="center"><em align="center">The REST API for smart teacher-student management</em></p>

<p align="center">
  <a href="https://codecov.io/gh/xlurio/aristotle-api" > 
    <img src="https://codecov.io/gh/xlurio/aristotle-api/branch/main/graph/badge.svg?token=EG0NHH2P0W" alt="Coverage"/> 
  </a>
  <a href="https://github.com/xlurio/aristotle-api/actions/workflows/test.yml">
    <img src="https://github.com/xlurio/aristotle-api/actions/workflows/test.yml/badge.svg" alt="Test"/>
  </a>
</p>


## Introduction

## Quick Start

Let's learn the fundamentals on the AristotleAPI by:
1. Creating a staff
2. Creating a teacher
3. Creating a student
4. Creating classroom with the teacher and the student as members
5. Register a grade
6. Register a absence
7. View student data
8. View teacher data

### Creating a Staff

First you will need to have access to a staff user, which can be created from the server console by using the following command:

```
$ python manage.py createsuperuser
Registration number: staff
Password:
```

Where `staff` is the chosen username. Now you'll need to create an authentication token for the staff user by using the following request:

```
POST /token HTTP/1.1
content-type: application/json

{
  "register": "staff",
  "password": "password"
}
```

If it works, you should receive the following response:

```
{
  "token": "12312h1j1nknwkqnkd1k12h13b21jb"
}
```

This token will be added to the `Authorization` header for creating the teachers, students and class rooms.

