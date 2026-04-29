import reflex as rx
from .components import navbar, footer
from .state import AppState


def page_shell(*children: rx.Component) -> rx.Component:
    """Authenticated page: shows navbar + guards unauthenticated users."""
    return rx.cond(
        AppState.token_is_valid,
        rx.el.div(
            navbar(),
            rx.el.main(
                *children,
                class_name="flex-1 flex flex-col items-center",
            ),
            footer(),
            class_name="min-h-screen flex flex-col bg-[#0e0e0e] text-white font-sans",
        ),
        # Not logged in — send to login page via JS redirect
        rx.el.div(
            rx.script("window.location.href='/'"),

            class_name="hidden",
        ),
    )


def auth_shell(*children: rx.Component) -> rx.Component:
    """Unauthenticated shell: no navbar, dark centered layout."""
    return rx.el.div(
        *children,
        class_name="min-h-screen flex flex-col items-center justify-center bg-[#0e0e0e] text-white font-sans",
    )