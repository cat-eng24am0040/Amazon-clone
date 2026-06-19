from itertools import product

from fastapi import FastAPI
from pydantic import BaseModel
import pickle

#Database connection
from db import users_collection
from db import products_collection
from db import cart_collection
from db import orders_collection



# Load the trained model

app = FastAPI()

with open("search_model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)


class User(BaseModel):
    name: str
    email: str
    password: str
class Login(BaseModel):
    email: str
    password: str


@app.get("/")
def home():
    return {
        "message": "Amazon AI Backend Running"
    }


@app.post("/register")
def register(user: User):

    users_collection.insert_one(user.model_dump())

    return {
        "message": "User Registered Successfully",
        "user": user
    }

@app.post("/login")
def login(login_data: Login):

    user = users_collection.find_one({
        "email": login_data.email
    })

    if not user:
        return {"message": "Invalid email"}

    if user["password"] != login_data.password:
        return {"message": "Invalid password"}

    user["_id"] = str(user["_id"])

    return {
        "message": "Login Successful",
        "user": user
    }
    
@app.get("/products")
def get_products():

    products = list(products_collection.find())

    for product in products:
        product["_id"] = str(product["_id"])

    return {"products": products}


@app.get("/product/{product_id}")
def get_product(product_id: int):

    product = products_collection.find_one({"id": product_id})

    if product:
        product["_id"] = str(product["_id"])
        return {"product": product}

    return {
        "message": "Product Not Found"
    }
@app.get("/search")
def search_products(q: str):

    results = []

    for product in products_collection.find():

        product["_id"] = str(product["_id"])

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

    product = products_collection.find_one({"id": product_id})

    if product:
        product["_id"] = str(product["_id"])

        return {
            "query": q,
            "predicted_product": product
        }

    return {
        "message": "No Product Found"
    }