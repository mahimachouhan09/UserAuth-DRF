# UserAuth-DRF
build a user authentication and authorization in django rest framework:

- User signup
- sign in
- logout
- forget password
- update password
- profile update

# Technology-Used
used 
- python,
- django rest framework
- database :- mysql

## How to use:
  - `pip install -r requirements.txt`
  - `python manage.py runserver`
  
## URLs to target:
  - to register a user
    - localhost:8000/api/auth/register
  - to login a user
    - localhost:8000/api/auth/login
  - to logout a user
    - localhost:8000/api/auth/logout
  - to change password
    - localhost:8000/api/auth/password_change
  - to forget password
    - localhost:8000/^password/reset/$
  - to update the user profile
    - localhost:8000/profile-update/

## Useful commands:
  - `python manage.py createsuperuser`
  - `python manage.py makemigrations`
  - `python manage.py migrate`
