import reflex as rx
from ..state import AppState


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            # Logo
            rx.el.div(
                rx.el.a(
                    rx.el.span("Drop", class_name="text-white font-bold text-2xl"),
                    rx.el.span("Keys", class_name="text-zinc-500 font-bold text-2xl"),
                    href="/home",
                    class_name="flex items-center",
                ),
                class_name="flex-1 flex justify-start",
            ),
            # Centered Navigation
            rx.el.div(
                rx.el.a(
                    "Home",
                    href="/home",
                    class_name="text-lg text-zinc-400 hover:text-white transition-colors duration-150 px-4",
                ),
                rx.el.a(
                    "Share",
                    href="/share",
                    class_name="text-lg text-zinc-400 hover:text-white transition-colors duration-150 px-4",
                ),
                rx.el.a(
                    "Unseal",
                    href="/unseal",
                    class_name="text-lg text-zinc-400 hover:text-white transition-colors duration-150 px-4",
                ),
                class_name="flex-1 flex justify-center items-center gap-4",
            ),
            # User & Logout
            rx.el.div(
                rx.el.span(
                    AppState.user_email,
                    class_name="text-base text-zinc-400 mr-4 hidden md:block",
                ),
                rx.el.button(
                    "Logout",
                    on_click=AppState.logout,
                    class_name=(
                        "text-sm px-4 py-2 rounded bg-zinc-200 text-zinc-900 font-bold "
                        "hover:bg-zinc-900/20 hover:text-zinc-100 hover:ring-1 hover:ring-zinc-600/80 "
                        "transition-all duration-150 cursor-pointer"
                    ),
                ),

                class_name="flex-1 flex justify-end items-center",
            ),
            class_name="max-w-7xl mx-auto px-8 h-24 flex items-center",

        ),
        class_name="w-full border-b border-zinc-800 bg-[#0e0e0e]",
    )