import streamlit as st

# await init_beanie(database=client.newbase, document_models=[Campaign])
# if st.session_state["mongo_connection_init"] = []

import asyncio
from typing import Optional
from beanie import Document, Indexed, init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic import Field


class Category(BaseModel):
    name: str
    description: str


class Campaign(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str] = None
    date: str  # You can also specify that a field should correspond to an index


async def init():
    if "mongo_connection_init" not in st.session_state:
        st.session_state.mongo_connection_init = True
        var_host = "Host"
        var_port = 18378
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await init_beanie(database=client.newbase, document_models=[Campaign])
