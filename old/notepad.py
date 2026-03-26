from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="LOTR Quotes")

sitater = {
    1: "One Ring to rule them all, One Ring to find them, One Ring to bring them all, and in the darkness bind them.",
    2: "Even the smallest person can change the course of the future.",
    3: "Not all those who wander are lost.",
    4: "You shall not pass!",
    5: "All we have to decide is what to do with the time that is given us.",
    6: "I will not say: do not weep; for not all tears are an evil.",
    7: "There’s some good in this world, Mr. Frodo, and it’s worth fighting for.",
    8: "My precious.",
    9: "Faithless is he that says farewell when the road darkens.",
    10: "The world is indeed full of peril and in it there are many dark places."
}

class GetQuote(BaseModel):
    quote: str

@app.get("/sitat", response_model=GetQuote)
def sitat():
    id = random.randint(1, len(sitater))
    return {"quote": sitater[id]}

@app.post("/sitat")
def add_sitat(data: Quote):
    new_id = len(sitater) + 1
    sitater[new_id] = data.quote
    return {
        "bleh"
        "id" : new_id
    }

