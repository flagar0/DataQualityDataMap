import streamlit as st
from datetime import datetime

# await init_beanie(database=client.newbase, document_models=[Campaign])
# if st.session_state["mongo_connection_init"] = []

from typing import Optional
from bunnet import Document


class Campaign(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str] = None
    date: str  # You can also specify that a field should correspond to an index
    dti: datetime
    dtf: datetime
    user_id: str
    collection_id: str
    public: str
    validated: str
    doi: Optional[str] = None
    location: Optional[str] = None  # "lat,lon" ex: "-23.5505,-46.6333"

    # class Settings:
    #     name = "products"
