"""Username and password screens for the persistent account workspace."""
import os
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from streamlit.errors import StreamlitSecretNotFoundError
from accounts import Accounts, AccountError
from ui import brand_panel


@st.cache_resource
def _cached_account_service(url, public, implementation_id):
    return Accounts(url or None, public=public)


def account_service(url, public):
    return _cached_account_service(url, public, id(Accounts))


account_service.clear = _cached_account_service.clear


def _database_settings():
    url = os.environ.get("SHOPIMPACT_DATABASE_URL", "")
    public = os.environ.get("SHOPIMPACT_PUBLIC", "false").lower() == "true"
    try:
        if "SHOPIMPACT_DATABASE_URL" not in os.environ:
            url = st.secrets.get("SHOPIMPACT_DATABASE_URL", url)
        if "SHOPIMPACT_PUBLIC" not in os.environ:
            public = bool(st.secrets.get("SHOPIMPACT_PUBLIC", public))
    except StreamlitSecretNotFoundError:
        pass
    return url, public


def require_account():
    url, public = _database_settings()
    try:
        service = account_service(url, public)
    except (AccountError, SQLAlchemyError):
        st.error("The account database is unavailable or not configured. Please contact the app owner.")
        st.stop()

    if st.session_state.get("auth_token"):
        try:
            saved = service.load(st.session_state.auth_token)
        except AccountError:
            st.session_state.clear()
            st.session_state["auth_notice"] = "Your session expired. Sign in again to open your saved purchases."
            st.rerun()
        except SQLAlchemyError:
            st.error("We cannot reach your saved data. Please try again shortly.")
            st.stop()
        if "account_data" not in st.session_state:
            st.session_state.account_data = saved
        return service, st.session_state.account_data

    introduction, authentication = st.columns([1, 1.08], gap="large")
    with introduction:
        brand_panel()
    with authentication:
        st.title("Welcome to ShopImpact")
        st.write("A fresh start, or right where you left off.")
        login, register = st.tabs(["Sign in", "Create account"])
        with login:
            with st.form("login"):
                name = st.text_input("Username", key="login_name", max_chars=40)
                password = st.text_input("Password", type="password", key="login_password", max_chars=128)
                if st.form_submit_button("Sign in", type="primary"):
                    try:
                        st.session_state.auth_token = service.login(name, password)
                        st.session_state.pop("account_data", None)
                        st.rerun()
                    except AccountError as error:
                        st.error(str(error))
                    except SQLAlchemyError:
                        st.error("Sign-in is temporarily unavailable. Please try again.")
        with register:
            with st.form("register", clear_on_submit=True):
                name = st.text_input("Choose a username", max_chars=40)
                password = st.text_input(
                    "Choose a password",
                    type="password",
                    max_chars=8,
                    help="Use 1–8 characters. Passwords are stored as Argon2id hashes.",
                )
                confirmation = st.text_input("Confirm password", type="password", max_chars=8)
                if st.form_submit_button("Create account", type="primary"):
                    created = False
                    try:
                        if password != confirmation:
                            raise AccountError("Passwords do not match.")
                        service.register_username_password(name, password)
                        created = True
                        st.session_state.auth_token = service.login(name, password)
                        st.session_state.pop("account_data", None)
                        st.rerun()
                    except AccountError as error:
                        st.error(str(error))
                    except SQLAlchemyError:
                        message = (
                            "Your account may have been created, but automatic sign-in failed. Try the Sign in tab."
                            if created else "We could not create the account. Please try again."
                        )
                        st.error(message)

        notice = st.session_state.pop("auth_notice", None)
        if notice:
            st.warning(notice)
        st.caption("Your account and purchases are saved in the app database. Passwords are stored as salted Argon2id hashes.")
    st.stop()


def sign_out(service):
    if st.session_state.get("auth_token"):
        try:
            service.logout(st.session_state.auth_token)
        except SQLAlchemyError:
            st.error("Sign-out is temporarily unavailable. Please try again.")
            return
    st.session_state.clear()
    st.rerun()


def save_account(service, data, purchases=None, settings=None):
    purchases = data["purchases"] if purchases is None else purchases
    settings = data["settings"] if settings is None else settings
    try:
        revision = service.save(st.session_state.auth_token, purchases, settings, data["revision"])
    except AccountError as error:
        st.error(str(error))
        return False
    except SQLAlchemyError:
        st.error("The change was not saved. Your previous data is safe; please try again.")
        return False
    data.update(purchases=purchases, settings=settings, revision=revision)
    return True
