import extra_streamlit_components as stx
import datetime
import streamlit as st


@st.cache(allow_output_mutation=True)
def get_manager(key):
    return stx.CookieManager(key=key)


def create_cookie(cookie_manager, key, value, datetime):
    return cookie_manager.set(key, value, expires_at=datetime)


def get_cookie(cookie_manager, key):
    return cookie_manager.get(key)
