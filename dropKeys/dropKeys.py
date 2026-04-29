import reflex as rx
from .pages import login, index, share, unseal
from .pages.login import auth_callback
from .state import AppState

from . import config

app = rx.App(
    theme=rx.theme(appearance="dark"),
    style={
        ".rt-Link:hover": {
            "color": "white !important",
            "text-decoration": "none",
        }
    }
)


app.add_page(login, route="/")
app.add_page(auth_callback, route="/auth/callback")
app.add_page(index, route="/home", on_load=AppState.load_home_data)
app.add_page(share, route="/share", on_load=AppState.reset_share)
app.add_page(unseal, route="/unseal")