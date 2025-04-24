## register account
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"email": "test1@gmail.com", "username": "testuser", "password": "Test1234!"}'

# verify email
curl http://localhost:8000/api/auth/verify-email/?token=edb9aed5-8543-45f0-82b8-365c7f07d5d6

## login
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "test2@example.com", "password": "Test1234!"}'

## profile access
curl http://localhost:8000/api/auth/profile/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDU5ODY5LCJpYXQiOjE3NDU0NTUwNjksImp0aSI6ImY3ZWFhMGRhYTI3YjQ4ODI4MDQ4ZDI5N2FkYzhjM2U3IiwidXNlcl9pZCI6M30.0UNB8b1F_BntsTv_jWUxV25zxkBf4sL4rZYzFBWIfZk"

## update profile
curl -X PUT http://localhost:8000/api/auth/profile/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDU4MTY0LCJpYXQiOjE3NDU0NTMzNjQsImp0aSI6ImRhZTMxMTRlZDY1MzQxYjdiZWU2NjhiYmM2Mzk1ZWEwIiwidXNlcl9pZCI6Mn0.aRyiAzQP1FxdqtzwDxXFRHlqWSeTw2qnKl_RH07_OfQ" -H "Content-Type: application/json" -d '{"address": "Nairobi, Kenya", "phone": "0712345674"}'

## password reset
curl -X POST http://localhost:8000/api/auth/password-reset/ -H "Content-Type: application/json" -d '{"email": "test1@gmail.com"}'

## password reset sending resposne
curl http://localhost:8000/api/auth/password-reset/confirm/?token=68c039b1-99af-4f81-9000-1e13af030063

## actual changing password

curl -X POST http://localhost:8000/api/auth/password-reset/confirm/ -H "Content-Type: application/json" -d '{"token": "68c039b1-99af-4f81-9000-1e13af030063", "new_password": "NewPass1234!"}'

## login with new creds:
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "test1@gmail.com", "password": "NewPass1234!"}'


curl http://localhost:8000/api/auth/verify-email/?token=230117b0-21cc-4a5c-9a47-4b164db45209

http://localhost:8000/api/auth/password-reset/confirm/?token=e91bb73b-4289-40aa-a36d-5ec465adbdb2

curl -X POST http://localhost:8000/api/auth/password-reset/confirm/ -H "Content-Type: application/json" -d '{"token": "e91bb73b-4289-40aa-a36d-5ec465adbdb2", "new_password": "Password@123"}'