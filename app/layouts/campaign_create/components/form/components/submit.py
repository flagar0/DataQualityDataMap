import streamlit as st
from datetime import datetime, date


from schemas import Campaign
from typing import Optional
from beanie import Document, Indexed, init_beanie
import uuid

import bunnet as bn

# class Task(Document):
#     content: str = Field(max_lenght=200)
#     is_complete: bool = Field(default=False)


# class Task(Document):
#     content: str = Field(max_lenght=200)
#     is_complete: bool = Field(default=False)


# class Category(BaseModel):
#     name: str
#     description: str


# class Campaign(Document):
#     name: str  # You can use normal types just like in pydantic
#     description: Optional[str] = None
#     date: str  # You can also specify that a field should correspond to an index


# This is an asynchronous example, so we will access it from an async function
def insert():
    client = st.session_state.mongo_client

    bn.init_bunnet(database=client.newbase, document_models=[Campaign])
    user = st.session_state.auth.user
    # # Beanie uses Motor async client under the hood
    # client = AsyncIOMotorClient("mongodb://localhost:27017")
    collectionname = "".join(
        e for e in str(st.session_state["campaign_name_input"]) if e.isalnum()
    )

    # # # Initialize beanie with the Product document class
    # await init_beanie(database=client.newbase, document_models=[Campaign])
    xdti: date = st.session_state["campaign_dates_input"][0]
    xdtf: date = st.session_state["campaign_dates_input"][1]
    Campaign1 = Campaign(
        name=str(st.session_state["campaign_name_input"]),
        date=xdti.isoformat() + " to " + xdtf.isoformat(),
        description=str(st.session_state["campaign_description_input"]),
        dti=datetime.combine(date=xdti, time=datetime.min.time()),
        dtf=datetime.combine(date=xdtf, time=datetime.min.time()),
        user_id=str(user),
        collection_id=collectionname + "_" + str(uuid.uuid4()),
    )
    # And can be inserted into the database
    Campaign1.insert()


def exec():
    insert()
    st.success(body="Submitted sucessfully")
