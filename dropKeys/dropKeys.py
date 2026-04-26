import reflex as rx
from .pages import login, index, share, unseal
from .pages.login import auth_callback

from . import config

app = rx.App(
    theme=rx.theme(appearance="dark"),
)

app.add_page(login, route="/")
app.add_page(auth_callback, route="/auth/callback")
app.add_page(index, route="/home")
app.add_page(share, route="/share")
app.add_page(unseal, route="/unseal")