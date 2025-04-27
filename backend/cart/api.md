# add to cart
curl -X POST http://localhost:8000/api/cart/add/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDY4NjM1LCJpYXQiOjE3NDU0NjM4MzUsImp0aSI6ImM5NjE1NTY4ODkxMTQ2NGE4M2FhNDU3YWE0ODMzZGQzIiwidXNlcl9pZCI6Mn0.6vmite5y9SbYNZ2JVmlAEFExna4lalrpHNCdOQ6fXvA" -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 1}'

## check cart
curl http://localhost:8000/api/cart/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDY4NjM1LCJpYXQiOjE3NDU0NjM4MzUsImp0aSI6ImM5NjE1NTY4ODkxMTQ2NGE4M2FhNDU3YWE0ODMzZGQzIiwidXNlcl9pZCI6Mn0.6vmite5y9SbYNZ2JVmlAEFExna4lalrpHNCdOQ6fXvA"

## remove form cart
curl -X DELETE http://localhost:8000/api/cart/remove/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDY4NjM1LCJpYXQiOjE3NDU0NjM4MzUsImp0aSI6ImM5NjE1NTY4ODkxMTQ2NGE4M2FhNDU3YWE0ODMzZGQzIiwidXNlcl9pZCI6Mn0.6vmite5y9SbYNZ2JVmlAEFExna4lalrpHNCdOQ6fXvA" -H "Content-Type: application/json" -d '{"product_id": 1}'