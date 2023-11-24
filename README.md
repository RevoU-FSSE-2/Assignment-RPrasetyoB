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

|              | Methods | Endpoint                   | Requirement & Authorization | Body                    |
|:------------ |:-------:|:--------------------------:|:------------------:|:-----------------------:|
| Register     | POST    | /auth/registration         | -                  | username, bio, password |
| Login        | POST    | /auth/login                | -                  | username, password      |
| Create Tweet | POST    | /tweet                     | bearer_token, user is_suspended? | tweet                   |
| User Profile | GET     | /user-profile              | bearer_token              | -                       |
| Follow       | POST    | /following/:target_user.id | bearer_token              | -                       |
| Flag spam    | POST    | /moderation/tweet          | bearer_token, moderator role     | tweet.id, is_spam       |
| Suspend user | POST    | /moderation/user           | bearer_token, moderator role     | user.id, is_suspended   |

### Some feature images :
- Suspended user in database: <br>

![Screenshot_3](https://github.com/RevoU-FSSE-2/Assignment-RPrasetyoB/assets/129088807/5057ebcd-8c8a-4da3-8962-baf613579a23)

- Suspended user cannot create tweet: <br>

![Screenshot_4](https://github.com/RevoU-FSSE-2/Assignment-RPrasetyoB/assets/129088807/73b50eb6-95d2-4076-962b-fe519ea6a50b)

- Flag Spam tweets in database: <br>

![Screenshot_2](https://github.com/RevoU-FSSE-2/Assignment-RPrasetyoB/assets/129088807/a20e1166-5bb3-477e-8e67-f02206c4c37e)


### User for Testing

- Moderator

```json
{
    "username":"rpb",
    "password":"rpb123"
}
```

- User

```json
{
    "username":"rpb2",
    "password":"rpb123"
}
```
