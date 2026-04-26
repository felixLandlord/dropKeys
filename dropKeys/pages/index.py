import reflex as rx
from ..state import AppState
from ..template import page_shell



def index() -> rx.Component:
    return page_shell(
        rx.el.div(
            rx.el.h1(
                "Activities",
                class_name=(
                    "text-5xl font-extrabold tracking-tight text-center "
                    "bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent"
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p("No recent activity", class_name="text-zinc-500 text-base"),
                    ),
                    class_name="p-8 border border-zinc-800 rounded text-center mt-10 bg-transparent",
                ),
                class_name="w-full",
            ),

            class_name="w-full max-w-3xl px-6 py-16",
            on_mount=AppState.load_home_data,
        ),
    )