import reflex as rx
from ..state import AppState
from ..template import page_shell



def activity_loading_overlay() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white mb-4 mx-auto"
            ),
            rx.el.p("Preparing unseal...", class_name="text-white text-xl font-medium tracking-tight"),
            rx.el.p("Locating document in vault", class_name="text-zinc-500 text-sm mt-2"),
            class_name="text-center p-8 rounded-2xl bg-zinc-900/50 backdrop-blur-xl border border-white/10 shadow-2xl",
        ),
        id="activity-loading-overlay",
        class_name="hidden fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-md transition-all duration-300",
    )

def index() -> rx.Component:
    return page_shell(
        activity_loading_overlay(),
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
                                # Left: name + meta
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(act["name"], class_name="text-zinc-100 font-medium text-sm truncate"),
                                        rx.cond(
                                            act["is_new"],
                                            rx.el.div(class_name="w-2 h-2 rounded-full bg-blue-500 shrink-0"),
                                            rx.fragment()
                                        ),
                                        class_name="flex items-center gap-2"
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            rx.cond(act["type"] == "Sent", "Sent to ", "From "),
                                            class_name="text-zinc-600 text-xs"
                                        ),
                                        rx.el.span(act["person"], class_name="text-zinc-400 text-xs"),
                                        class_name="flex items-center gap-1 mt-0.5 flex-wrap"
                                    ),
                                    class_name="flex-1 min-w-0"
                                ),
                                # Right: date + unseal button
                                rx.el.div(
                                    rx.el.span(act["date"], class_name="text-zinc-600 text-xs whitespace-nowrap"),
                                    rx.el.button(
                                        "Unseal",
                                        on_click=lambda: [
                                            rx.call_script("document.getElementById('activity-loading-overlay').classList.remove('hidden')"),
                                            AppState.view_activity(act["comp_key"])
                                        ],
                                        class_name=(
                                            "ml-4 px-3 py-1 text-xs font-medium rounded border border-zinc-600 "
                                            "text-zinc-300 hover:border-zinc-100/80 hover:text-zinc-100 "
                                            "transition-all duration-150 whitespace-nowrap"
                                        ),
                                    ),
                                    class_name="flex items-center gap-3 shrink-0 ml-4"
                                ),
                                class_name="flex items-center justify-between px-5 py-3 border-b border-zinc-800 last:border-0"
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