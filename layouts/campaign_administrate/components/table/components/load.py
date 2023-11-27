import streamlit as st
import pandas as pd

# import config.init_state

import asyncio
from typing import Optional
from beanie import Document, Indexed, init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic import Field

user_id = "a"

# st.session_state["table_data"] = ""


class Campaign(Document):
    name: str  # You can use normal types just like in pydantic
    description: Optional[str] = None
    date: str  # You can also specify that a field should correspond to an index


async def example():
    # Beanie uses Motor async client under the hood
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    # Initialize beanie with the Product document class
    await init_beanie(database=client.newbase, document_models=[Campaign])

    campaigns_list = [Campaign]

    result = await Campaign.find_all().to_list()
    # campaigns_list = Campaign.find_all()

    return result


async def delete(delete):
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    # Initialize beanie with the Product document class
    await init_beanie(database=client.newbase, document_models=[Campaign])

    await Campaign.find_one(Campaign.name == delete).delete()


def render():
    st.session_state.table_data = st.session_state.get("table_data", [])

    campaigns_list = [Campaign]

    campaigns_list = asyncio.run(example())

    # Read Operation
    # st.header("Read Operation")
    # if st.button("Refresh Users"):
    #     users = await User.all()
    #     for user in users:
    #         st.write(f"Name: {user.name}, Age: {user.age}")

    # Update Operation
    # st.header("Update Operation")
    # name_update = st.text_input("Enter Campaign to Update:")
    # new_duration_update = st.number_input("Enter New Age:")
    # if st.button("Update User"):
    #     user_to_update = await User.find_one({"name": name_update})
    #     if user_to_update:
    #         user_to_update.age = new_age_update
    #         await user_to_update.update()
    #         st.success(f"User {user_to_update.name} updated successfully!")
    #     else:
    #         st.error("User not found.")

    # # Delete Operation
    # st.header("Delete Operation")
    # name_delete = st.text_input("Enter Name to Delete:")
    # if st.button("Delete User"):
    #     await connect_to_mongo()
    #     user_to_delete = await User.find_one({"name": name_delete})
    #     if user_to_delete:
    #         await user_to_delete.delete()
    #         st.success(f"User {user_to_delete.name} deleted successfully!")
    #     else:
    #         st.error("User not found.")
    if st.button("load"):
        st.session_state.table_data = st.session_state.clear
        st.session_state.table_data = []
        for campaign in campaigns_list:
            Campaign_name = campaign.name
            description = campaign.description
            date = campaign.date

            st.session_state.table_data.append((Campaign_name, description, date))

    # delete_options = [""] + [
    #     f"{data[1]} - {data[2]}" for data in st.session_state.table_data
    # ]

    delete_options = [f"{data[0]}" for data in st.session_state.table_data]
    selected_delete = st.selectbox("Select the item for deletion", delete_options)

    if st.button("Delete Item"):
        if selected_delete and selected_delete != "":
            # Remove selected item from table data
            selected_index = delete_options.index(selected_delete) - 1
            if selected_index >= 0:
                asyncio.run(delete(selected_delete))
                st.session_state.table_data.pop(selected_index)

    if st.session_state.table_data:
        df = pd.DataFrame(
            st.session_state.table_data,
            columns=["Name", "Description", "Date"],
        )
        st.write(df)
