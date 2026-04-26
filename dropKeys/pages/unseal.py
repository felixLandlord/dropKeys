import reflex as rx
from ..template import page_shell
from ..state import AppState


def unseal() -> rx.Component:
    return page_shell(
        rx.el.div(
            rx.el.h1(
                "Decrypt a document",
                class_name=(
                    "text-5xl font-extrabold tracking-tight text-center "
                    "bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent"
                ),
            ),

            # ID input
            rx.el.div(
                rx.el.span("ID", class_name="block text-xs font-medium text-zinc-100"),
                rx.el.input(
                    placeholder="",
                    value=AppState.unseal_id,
                    on_change=AppState.set_unseal_id,
                    class_name=(
                        "w-full p-0 text-base bg-transparent border-0 appearance-none "
                        "text-zinc-100 placeholder-zinc-500 focus:ring-0 focus:outline-none sm:text-sm"
                    ),

                ),
                class_name=(
                    "mt-10 w-full h-16 px-3 py-2 duration-150 border rounded "
                    "border-zinc-600 hover:border-zinc-100/80 focus-within:border-zinc-100/80"
                ),
            ),

            # Unseal button
            rx.el.button(
                rx.cond(AppState.unseal_loading, "Decrypting…", "Unseal"),
                on_click=AppState.do_unseal,
                disabled=AppState.unseal_loading | (AppState.unseal_id == ""),
                class_name=(
                    "mt-6 w-full h-12 inline-flex justify-center items-center transition-all "
                    "rounded px-4 py-1.5 md:py-2 text-base font-semibold bg-zinc-200 "
                    "text-zinc-900 enabled:hover:bg-zinc-900/20 enabled:hover:text-zinc-100 "
                    "enabled:hover:ring-1 enabled:hover:ring-zinc-600/80 duration-150 "
                    "disabled:opacity-40 disabled:cursor-not-allowed"
                ),

            ),


            # Error
            rx.cond(
                AppState.unseal_error != "",
                rx.el.p(
                    AppState.unseal_error,
                    class_name="mt-4 text-sm text-red-400",
                ),
                rx.fragment(),
            ),

            # Result
            rx.cond(
                AppState.unsealed_content != "",
                rx.el.div(
                    rx.el.p(
                        "Decrypted content:",
                        class_name="text-xs text-zinc-400 mb-2",
                    ),
                    rx.el.pre(
                        AppState.unsealed_content,
                        class_name=(
                            "text-sm text-emerald-400 font-mono whitespace-pre-wrap break-all"
                        ),
                    ),
                    rx.el.button(
                        "Decrypt another",
                        on_click=AppState.reset_unseal,
                        class_name=(
                            "mt-4 text-xs text-zinc-500 underline hover:text-zinc-300 transition-colors"
                        ),
                    ),
                    class_name=(
                        "mt-6 p-4 rounded-lg border border-emerald-800 bg-emerald-950/30 w-full"
                    ),
                ),
                rx.fragment(),
            ),

            class_name="w-full max-w-3xl px-6 py-16",
        ),
    )