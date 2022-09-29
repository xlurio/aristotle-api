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

## Quick start

Let's learn the fundamentals on the AristotleAPI by:
1. Creating a staff
2. Creating a teacher
3. Creating a student
4. Creating classroom with the teacher and the student as members
5. Register a grade
6. Register a absence
7. View student data
8. View teacher data

### Creating a staff

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


### Creating a teacher

Now let's create user for the teacher of our class. With the authentication token for the staff user, we can make following request:

```
POST /users HTTP/1.1
content-type: application/json
Authentication: token 12312h1j1nknwkqnkd1k12h13b21jb

{
  "first_name": "Chloe",
  "last_name": "Moretz",
  "password": "teacherpass",
  "role": "teacher"
}
```

The response should something like:

```
{
  "id": 1,
  "register": "chloe-h1j23k1j23k",
  "first_name": "Chloe",
  "last_name": "Moretz"
}
```

### Creating a student

Let's also create our student:

```
POST /users HTTP/1.1
content-type: application/json
Authentication: token 12312h1j1nknwkqnkd1k12h13b21jb

{
  "first_name": "Ryan",
  "last_name": "Gosling",
  "password": "studentpass",
  "role": "student"
}
```


The response should something like:

```
{
  "id": 2,
  "register": "ryan-h1j23k1j23k",
  "first_name": "Ryan",
  "last_name": "Gosling"
}
```


## Creating a classroom

Finally, let's create our class room. For that we will make the following request:

```
POST /classrooms HTTP/1.1
content-type: application/json
Authentication: token 12312h1j1nknwkqnkd1k12h13b21jb

{
  "subject": "physics",
  "members": [1, 2],
  "start": "2022-08-10",
  "deadline": "2022-12-10"
}
```

Being `1` the ID of the teacher and `2` the ID of the student.