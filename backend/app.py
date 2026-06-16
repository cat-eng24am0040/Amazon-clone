from fastapi import FastAPI
from pydantic import BaseModel
import pickle

# Load the trained model

app = FastAPI()

with open("search_model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)


users = []

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


class User(BaseModel):
    name: str
    email: str
    password: int
class Login(BaseModel):
    email: str
    password: int


@app.get("/")
def home():
    return {
        "message": "Amazon AI Backend Running"
    }


@app.post("/register")
def register(user: User):

    users.append(user.model_dump())

    return {
        "message": "User Registered Successfully",
        "user": user
    }
@app.post("/login")
def login(email: str, password: int):
    for user in users:
        if user['email'] == email :
            if user['password'] == password:
              return {
                "message": "Login Successful",
                "user": user
            }
            return{
                "message": "Invalid password"
            }
    return {
        "message": "Invalid email or password"
    }
@app.get("/products")
def get_products():

    return {
        "products": products
    }
@app.get("/product/{product_id}")
def get_product(product_id: int):

    for product in products:

        if product["id"] == product_id:

            return {
                "product": product
            }

    return {
        "message": "Product Not Found"
    }
@app.get("/search")
def search_products(q: str):

    results = []

    for product in products:

        if q.lower() in product["name"].lower():

            results.append(product)

    return {
        "query": q,
        "results": results
    }
@app.get("/ai-search")
def ai_search(q: str):

    query_vector = vectorizer.transform([q])

    prediction = model.predict(query_vector)

    product_id = int(prediction[0])

    for product in products:

        if product["id"] == product_id:

            return {
                "query": q,
                "predicted_product": product
            }

    return {
        "message": "No Product Found"
    }