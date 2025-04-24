Add Sample Categories and Products
Since the database may be reset, let’s re-add the 5 sample products and categories via the Django admin.
Categories
Floral

Woody

Citrus

Spicy

Herbal

Products
Lavender Glow:
Category: Floral

Price: KES 1500.00

Stock: 50

Description: A soothing lavender-scented candle for relaxation.

Sandalwood Serenity:
Category: Woody

Price: KES 2000.00

Stock: 30

Description: A warm sandalwood candle with earthy notes.

Citrus Burst:
Category: Citrus

Price: KES 1200.00

Stock: 40

Description: A refreshing lemon-orange candle to uplift your mood.

Cinnamon Spice:
Category: Spicy

Price: KES 1800.00

Stock: 25

Description: A cozy cinnamon-scented candle for festive evenings.

Eucalyptus Breeze:
Category: Herbal

Price: KES 1600.00

Stock: 35

Description: A refreshing eucalyptus candle for clarity and calm.

Add via Django Admin
Start the server:
bash

python manage.py runserver

Visit http://localhost:8000/admin/, log in with admin@example.com/Admin1234!.

Add Categories:
Go to Products > Categories > Add Category.

Add each: Floral, Woody, Citrus, Spicy, Herbal (Name only; no parent field).

Add Products:
Go to Products > Products > Add Product.

For each product (e.g., Lavender Glow):
Name: Lavender Glow

Description: A soothing lavender-scented candle for relaxation.

Price: 1500.00

Stock: 50

Category: Floral

Photo: Optional (skip or upload a .jpg).

Save each.

