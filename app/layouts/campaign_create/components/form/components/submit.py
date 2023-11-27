import streamlit as st
import datetime


import asyncio
from typing import Optional
from beanie import Document, Indexed, init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic import Field


class Task(Document):
    content: str = Field(max_lenght=200)
    is_complete: bool = Field(default=False)


class Task(Document):
    content: str = Field(max_lenght=200)
    is_complete: bool = Field(default=False)


class Category(BaseModel):
    name: str
    description: str


class Campaign(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str] = None
    date: str  # You can also specify that a field should correspond to an index


# This is an asynchronous example, so we will access it from an async function
async def example():
    # Beanie uses Motor async client under the hood
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    # Initialize beanie with the Product document class
    await init_beanie(database=client.newbase, document_models=[Campaign])

    Campaign1 = Campaign(
        name=str(st.session_state["campaign_name_input"]),
        date=str(st.session_state["campaign_dates_input"]),
        description=str(st.session_state["campaign_description_input"]),
    )
    # And can be inserted into the database
    await Campaign1.insert()


def exec():
    asyncio.run(example())
    st.success(body="Submitted sucessfully")
