import reflex as rx
from ..template import page_shell
from ..state import AppState


def unseal() -> rx.Component:

    return page_shell(
        rx.el.div(
            rx.cond(
                AppState.unsealed_content == "",
                # Input View
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
                        rx.cond(
                            AppState.unseal_loading, 
                            rx.icon(tag="settings", class_name="animate-spin text-zinc-900"),
                            "Unseal"
                        ),
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
                            class_name="mt-4 text-sm text-red-400 text-center",
                        ),
                        rx.fragment(),
                    ),
                    class_name="w-full max-w-3xl px-6 py-16",
                ),
                # Success View
                rx.el.div(
                    # Reads Left
                    rx.cond(
                        AppState.unseal_reads_left != None,
                        rx.el.div(
                            rx.cond(
                                AppState.unseal_reads_left > 0,
                                rx.el.p(
                                    "This document can be read ",
                                    rx.el.span(AppState.unseal_reads_left.to_string(), class_name="text-zinc-100"),
                                    " more times.",
                                    class_name="text-zinc-600"
                                ),
                                rx.el.p(
                                    "This was the last time this document could be read. It was deleted from storage.",
                                    class_name="text-zinc-400"
                                ),
                            ),
                            class_name="text-sm text-center mb-8"
                        ),
                        rx.fragment()
                    ),

                    # Decrypted box
                    rx.el.pre(
                        rx.el.div(
                            # Line numbers
                            rx.el.div(
                                rx.foreach(
                                    AppState.line_numbers_unseal, # I'll need to define this or reuse
                                    lambda n: rx.el.span(n, class_name="block"),
                                ),
                                aria_hidden="true",
                                class_name="pr-4 font-mono border-r select-none border-zinc-300/5 text-zinc-700",
                            ),
                            # Content
                            rx.el.div(
                                rx.el.code(
                                    AppState.unsealed_content,
                                    class_name="px-4 text-left whitespace-pre-wrap break-all"
                                ),
                                class_name="flex overflow-x-auto"
                            ),
                            class_name="flex items-start px-4 py-3 text-sm",
                        ),
                        class_name=(
                            "w-full rounded border border-zinc-600 bg-transparent text-zinc-100 font-mono"
                        ),
                    ),

                    # Buttons
                    rx.el.div(
                        rx.el.button(
                            "Share another",
                            on_click=rx.redirect("/share"),
                            class_name=(
                                "relative inline-flex items-center px-4 py-2 text-sm font-medium "
                                "duration-150 border rounded text-zinc-300 border-zinc-300/40 "
                                "hover:border-zinc-300 focus:outline-none hover:text-white"
                            ),
                        ),
                        rx.el.button(
                            rx.cond(
                                AppState.unseal_copied,
                                rx.el.div(
                                    rx.icon(tag="clipboard-check", size=16),
                                    rx.el.span("Copied"),
                                    class_name="flex items-center gap-2",
                                ),
                                rx.el.div(
                                    rx.icon(tag="clipboard", size=16),
                                    rx.el.span("Copy"),
                                    class_name="flex items-center gap-2",
                                ),
                            ),
                            on_click=AppState.copy_unsealed_content,
                            class_name=(
                                "relative inline-flex items-center px-4 py-2 text-sm font-medium "
                                "duration-150 border rounded text-zinc-700 border-zinc-300 "
                                "bg-zinc-50 hover focus:border-zinc-500 focus:outline-none "
                                "hover:text-zinc-50 hover:bg-zinc-900"
                            ),
                        ),
                        class_name="flex items-center justify-end gap-4 mt-4 w-full"
                    ),
                    class_name="w-full max-w-4xl px-6 py-16",
                )
            ),
            class_name="w-full flex flex-col items-center",
        ),
    )