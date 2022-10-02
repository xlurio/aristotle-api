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

The AristotleAPI is a REST API that provides a smart management of students grades and absences for schools and colleges. Currently it has the following features:

* Administrators can register teachers
* Administrators can register students
* Administrators can register class rooms
* Teachers can register grades
* Teachers can register absences
* Teachers can list all the data about the classes this teaches
* Students can list all the data about the classes this attends


## Requirements

* Python 3.8+
* django
* djangorestframework
* drf-spectacular
* drf-spectacular-sidecar
* gunicorn


## Quick start

Let's learn the fundamentals on the AristotleAPI.


### Running

To launch the API locally, you can run the following command in the root folder:

```
$ gunicorn
```

**Warning: this method is not recommended for application at production**


### Creating a staff

First you will need to have access to a staff user, which can be created from the server console by using the following command:

```
$ python manage.py createsuperuser
Registration number: staff
Password:
```

Where `staff` is the chosen username. 


### Authenticating as staff

Now you'll need to create an authentication token for the staff user by using the following request:

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


### Creating a classroom

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

Being `1` the ID of the teacher and `2` the ID of the student. The response should be something like:

```
{
  "id": 1,
  "subject": "physics",
  "name": "physics-112u312981e",
  "members": [
    1, 2
  ],
  "school_days": 100,
  "start": "2022-08-10",
  "deadline": "2022-12-10"
}
```


### Authenticating as teacher

Now let's become a teacher. We will get the authentication token for the teacher user by making the following request:

```
POST /token HTTP/1.1
content-type: application/json

{
  "register": "chloe-h1j23k1j23k",
  "password": "teacherpass"
}
```

If it works, you should receive the following response:

```
{
  "token": "dshjqkh3j4h2k3b42k3b4"
}
```

This token will be added to the `Authorization` header for registering grades and absences.


### Registering grade

For registering a grade for the created student, we will use the `/grades` end point, by making a request as the following:

```
POST /grades HTTP/1.1
content-type: application/json
Authentication: token dshjqkh3j4h2k3b42k3b4

{
  "title": "Test 1",
  "grade": 90,
  "student": 2,
  "classroom": 1
}
```

Being `2` the ID to the student user, `1` the class room ID, `Test 1` the title of the grade and `90` the grade value. The response should be something like:

```
{
  "id": 1,
  "title": "Test 1",
  "grade": 90,
  "student": 2,
  "classroom": 1
}
```


### Registering absence

or registering an absence for the created student, we will use the `/absence` end point, by making a request as the following:

```
POST /absence HTTP/1.1
content-type: application/json
Authentication: token dshjqkh3j4h2k3b42k3b4

{
  "absence_date": "2022-09-29",
  "classroom": 1,
  "student": 2
}
```

Being `2` the ID to the student user, `1` the class room ID and `2022-09-29` the date of the absence. The response should be something like:

```
{
  "id": 1,
  "absence_date": "2022-09-29",
  "classroom": 1,
  "student": 2
}
```


### List teacher data

For checking the teacher class rooms data, you can use the `/teacher/classrooms` end point, by make a GET request:

```
GET /teacher/classrooms HTTP/1.1
content-type: application/json
Authentication: token dshjqkh3j4h2k3b42k3b4
```

And the response should be something like:

```
[
  {
    "id": 1,
    "classroom": "physics-112u312981e",
    "students": [
      {
        "student": "Ryan Gosling",
        "grades": [
          {
            "average": 90,
            "grade_values": [
              {
                "title": "Test 1",
                "grade_value": 90
              }
            ]
          }
        ],
        "absence": [
          {
            "absence_amount": 1,
            "frequency": 0.99,
            "absence_dates": [
              {
                "absence_date": "2022-09-29"
              }
            ]
          }
        ]
      }
    ]
  }
]
```


### Retrieve teacher data

You can also retrieve only the information about a specific class on the same end point by passing the teacher class room id as following:

```
GET /teacher/classrooms/1 HTTP/1.1
content-type: application/json
Authentication: token dshjqkh3j4h2k3b42k3b4
```

And the response should be something like:

```
{
  "id": 1,
  "classroom": "physics-112u312981e",
  "students": [
    {
      "student": "Ryan Gosling",
      "grades": [
        {
          "average": 90,
          "grade_values": [
            {
              "title": "Test 1",
              "grade_value": 90
            }
          ]
        }
      ],
      "absence": [
        {
          "absence_amount": 1,
          "frequency": 0.99,
          "absence_dates": [
            {
              "absence_date": "2022-09-29"
            }
          ]
        }
      ]
    }
  ]
}
```

### Authenticating as student

Now let's become a student. We will get the authentication token for the student user by making the following request:

```
POST /token HTTP/1.1
content-type: application/json

{
  "register": "ryan-h1j23k1j23k",
  "password": "studentpass"
}
```

If it works, you should receive the following response:

```
{
  "token": "duidh1ui2e1u2h3i1hi12"
}
```

This token will be added to the `Authorization` header for viewing the student data


### Listing student data


For checking the student class rooms data, you can use the `/student/classrooms` end point, by make a GET request:

```
GET /student/classrooms HTTP/1.1
content-type: application/json
Authentication: token duidh1ui2e1u2h3i1hi12
```

And the response should be something like:

```
[
  {
    "id": 1,
    "classroom": "physics-112u312981e",
    "grades": [
      {
        "average": 90,
        "grade_values": [
          {
            "title": "Test 1",
            "grade_value": 90
          }
        ]
      }
    ],
    "absences": [
      {
        "absence_amount": 1,
        "frequency": 0.99,
        "absence_dates": [
          {
            "absence_date": "2022-09-29"
          }
        ]
      }
    ]
  }
]
```


### Retrieve student data

You can also retrieve only the information about a specific class on the same end point by passing the student class room id as following:

```
GET /student/classrooms/1 HTTP/1.1
content-type: application/json
Authentication: token duidh1ui2e1u2h3i1hi12
```

And the response should be something like:

```
{
  "id": 1,
  "classroom": "physics-112u312981e",
  "grades": [
    {
      "average": 90,
      "grade_values": [
        {
          "title": "Test 1",
          "grade_value": 90
        }
      ]
    }
  ],
  "absences": [
    {
      "absence_amount": 1,
      "frequency": 0.99,
      "absence_dates": [
        {
          "absence_date": "2022-09-29"
        }
      ]
    }
  ]
}
```

## License

This project is licensed under the terms of the MIT license.
