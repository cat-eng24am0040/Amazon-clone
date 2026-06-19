from db import products_collection

products = [
    {
        "id": 1,
        "name": "Apple iPhone 15",
        "price": 79999,
        "rating": 4.7
    },
    {
        "id": 2,
        "name": "Samsung Galaxy S24",
        "price": 74999,
        "rating": 4.6
    },
    {
        "id": 3,
        "name": "OnePlus 12",
        "price": 59999,
        "rating": 4.5
    },
    {
        "id": 4,
        "name": "Apple MacBook Air M3",
        "price": 114999,
        "rating": 4.8,
        "description": "13-inch Laptop"
    },
    {
        "id": 5,
        "name": "Apple AirPods Pro",
        "price": 24999,
        "rating": 4.7,
        "description": "Wireless Earbuds"
    }
]

products_collection.insert_many(products)

