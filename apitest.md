## register account
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"email": "test1@gmail.com", "username": "testuser", "password": "Test1234!"}'

# verify email
curl http://localhost:8000/api/auth/verify-email/?token=edb9aed5-8543-45f0-82b8-365c7f07d5d6

## login
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "test1@gmail.com", "password": "Test1234!"}'

## profile access
curl http://localhost:8000/api/auth/profile/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDY0NTczLCJpYXQiOjE3NDU0NTk3NzMsImp0aSI6IjZjNDNkM2FmZmY1MjQ3ZmRiMGQ5NTIwMDZkZjE5MmQzIiwidXNlcl9pZCI6Mn0.Tn4gLxXQlAEVcJyJnx_m0Q278_aRcRFOnyNYfbeMuUc"

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

## logout

curl -X POST http://localhost:8000/api/auth/logout/ -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDY5ODc0LCJpYXQiOjE3NDU0NjUwNzQsImp0aSI6ImU0MmUzNmRkMWM3YzQ1NzI4Y2YwZTIzNTY4YjQ1ZjVkIiwidXNlcl9pZCI6Mn0.5auVVxCzGqfPv0zbD00RdDJahILqQvpbegGb5iReQEA" -d '{"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NjY3NDY3NCwiaWF0IjoxNzQ1NDY1MDc0LCJqdGkiOiI0ZDdjNDIzMjNhZDI0MGUyYjE1ZGVkYjI0Nzg1MmQ3MSIsInVzZXJfaWQiOjJ9.DC25-fhZOYWM4uRpTtwzK9R7jYcqP65IiH50IFwcyBg"}'


## optin to receive stock alerts
curl -X PUT http://localhost:8000/api/auth/profile/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDYyMTE0LCJpYXQiOjE3NDU0NTczMTQsImp0aSI6ImFmODcxMWE3MDhjZTRiODBiYTQ3NmRhMjMzYTQ4MjI4IiwidXNlcl9pZCI6Mn0.SXJT95sUoNl-XiNsQ8IYUW3K0QzGsKwsW0cRtzUy7qA" -H "Content-Type: application/json" -d '{"receive_stock_alerts": true}'
