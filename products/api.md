curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email": "david@gmail.com", "password": "kali"}'


## add categories
curl -X POST http://localhost:8000/api/products/categories/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDYwNDUxLCJpYXQiOjE3NDU0NTU2NTEsImp0aSI6IjIwOGM4OTAyODZlYTRkYjJiYWUxZGZiNmYyOTc0ODFjIiwidXNlcl9pZCI6MX0.wtTwaxqSyB7vKyY3PyjJUumMHnLZ0tV8LYZkU21t22U" -H "Content-Type: application/json" -d '{"name": "Floral"}'

## list categories
curl http://localhost:8000/api/products/categories/

## create product
curl -X POST http://localhost:8000/api/products/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDYwNDUxLCJpYXQiOjE3NDU0NTU2NTEsImp0aSI6IjIwOGM4OTAyODZlYTRkYjJiYWUxZGZiNmYyOTc0ODFjIiwidXNlcl9pZCI6MX0.wtTwaxqSyB7vKyY3PyjJUumMHnLZ0tV8LYZkU21t22U" -H "Content-Type: application/json" -d '{"name": "Lavender Glow", "description": "A soothing lavender candle", "price": 1500.00, "stock": 50, "category_id": 1}'


## update a prodcut:
curl -X PUT http://localhost:8000/api/products/1/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDYwNDUxLCJpYXQiOjE3NDU0NTU2NTEsImp0aSI6IjIwOGM4OTAyODZlYTRkYjJiYWUxZGZiNmYyOTc0ODFjIiwidXNlcl9pZCI6MX0.wtTwaxqSyB7vKyY3PyjJUumMHnLZ0tV8LYZkU21t22U" -H "Content-Type: application/json" -d '{"name": "Lavender Glow", "description": "Updated description", "price": 1600.00, "stock": 40, "category_id": 1}'


## delete a product
curl -X DELETE http://localhost:8000/api/products/1/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MDYwNDUxLCJpYXQiOjE3NDU0NTU2NTEsImp0aSI6IjIwOGM4OTAyODZlYTRkYjJiYWUxZGZiNmYyOTc0ODFjIiwidXNlcl9pZCI6MX0.wtTwaxqSyB7vKyY3PyjJUumMHnLZ0tV8LYZkU21t22U"