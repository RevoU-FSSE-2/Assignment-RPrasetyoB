# Twitter-like Bank End project

This is a backend application for a Twitter-like platform, built using Flask and SQLAlchemy. The backend provides essential functionalities such as user registration, tweet creation, user profiles, and moderation actions.

## Features

- **User Registration**: Allows users to register with unique usernames, bio, and passwords.

- **User Login**: Allows users to login.

- **User Authentication**: Secures endpoints with JWT-based authentication, ensuring user data remains private.

- **Tweet Creation**: Enables users to create tweets with a character limit of 150.

- **User Profiles**: Provides user profiles displaying basic information, following status, and their tweets.

- **Follow System**: Allows users to follow and unfollow each other.

- **Moderation Actions**: Moderators can suspend users, flag tweets as spam, and perform other administrative actions.
  
  
  

## Instalation

1. Clone the repository:
   
   ```
   git clone https://github.com/RevoU-FSSE-2/Assignment-RPrasetyoB.git
   ```

2. Install dependencies:
   
   ```
   pip install pipenv
   ```
   
   ```
   pipenv shell
   ```
   
   ```
   pipenv install
   ```

3. Run the application:
   
   ```
   flask run
   ```



## API Endpoint

#### API documentation:

https://documenter.getpostman.com/view/29092304/2s9YeD7sxj



#### Postman file :

[week21.postman_collection.json - Google Drive](https://drive.google.com/file/d/1I-ZAI0Ltrneg7fRYU1R4NQBLAEKiKoBb/view?usp=sharing)

|              | Methods | Endpoint                   | Authorization      | Body                    |
|:------------ |:-------:|:--------------------------:|:------------------:|:-----------------------:|
| Register     | POST    | /auth/registration         | -                  | username, bio, password |
| Login        | POST    | /auth/login                | -                  | username, password      |
| Create Tweet | POST    | /tweet                     | user is_suspended? | tweet                   |
| User Profile | GET     | /user-profile              | token              | -                       |
| Follow       | POST    | /following/:target_user.id | token              | -                       |
| Flag spam    | POST    | /moderation/tweet          | moderator role     | tweet.id, is_spam       |
| Suspend user | POST    | /moderation/user           | moderator role     | user.id, is_suspended   |

### User for Testing

- Moderator

```json
{
    "username":"rpb",
    "password":"rpb123"
}
```

- user

```json
{
    "username":"rpb2",
    "password":"rpb123"
}
```
