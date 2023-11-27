import streamlit as st


def exec():
    flag_required = []
    if (
        st.session_state["campaign_name_input"] is None
        and st.session_state["campaign_name_input"] == ""
    ):
        flag_required.append("Campaign Name")

    if st.session_state["campaign_dates_input"] == [None, None]:
        return flag_required.append("Campain dates")

    if flag_required:
        st.error(body=f"Required fields missing: {flag_required}")
        return False
