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
                rx.cond(
                    AppState.activities.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            AppState.activities,
                            lambda act: rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(act["name"], class_name="text-zinc-100 font-semibold block text-base"),
                                        rx.el.span(
                                            rx.cond(
                                                act["type"] == "Sent",
                                                f"To: {act['person']}",
                                                f"From: {act['person']}"
                                            ),
                                            class_name="text-zinc-500 text-xs mt-1"
                                        ),
                                        class_name="flex-1"
                                    ),
                                    rx.el.div(
                                        rx.el.span(act["date"], class_name="text-zinc-500 text-xs mr-4"),
                                        rx.el.span(">", class_name="text-zinc-500 font-bold"),
                                        class_name="flex items-center"
                                    ),
                                    class_name="flex items-center justify-between p-6 hover:bg-zinc-800/30 transition-colors cursor-pointer",
                                    on_click=lambda: AppState.view_activity(act["comp_key"])
                                ),

                                class_name="border-b border-zinc-800 last:border-0"
                            )
                        ),
                        class_name="w-full bg-transparent h-full"
                    ),
                    rx.el.div(
                        rx.el.p("No recent activity", class_name="text-zinc-500 text-base"),
                        class_name="flex items-center justify-center h-full w-full flex-1"
                    )
                ),
                class_name="w-full border border-zinc-600 rounded mt-12 bg-transparent overflow-hidden min-h-[400px] flex flex-col",
            ),








            class_name="w-full max-w-3xl px-6 py-16",
            on_mount=AppState.load_home_data,
        ),
    )