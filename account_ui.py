"""Session-only workspace state for the no-sign-in app."""
import streamlit as st


DEFAULT_WORKSPACE = {
    "username": "Guest",
    "purchases": [],
    "settings": {
        "budget": 10000.0,
        "carbon_goal": 100,
        "contrast": False,
        "wishlist": [],
    },
    "revision": 0,
}


def guest_workspace():
    """Create an isolated workspace for this Streamlit browser session."""
    if "account_data" not in st.session_state:
        st.session_state["account_data"] = {
            **DEFAULT_WORKSPACE,
            "purchases": [],
            "settings": dict(DEFAULT_WORKSPACE["settings"]),
        }
    return st.session_state["account_data"]


def save_workspace(workspace, purchases=None, settings=None):
    """Update this session's workspace; it is not saved to a database."""
    purchases = workspace["purchases"] if purchases is None else purchases
    settings = workspace["settings"] if settings is None else settings
    if len(purchases) > 1000:
        st.error("This workspace supports 1,000 purchases. Export a backup before starting a new one.")
        return False
    workspace.update(purchases=purchases, settings=settings)
    st.session_state["account_data"] = workspace
    return True
