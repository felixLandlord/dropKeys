import reflex as rx
from ..template import page_shell
from ..state import AppState


def _ttl_select() -> rx.Component:
    return rx.el.select(
        rx.el.option("Minutes", value="Minutes"),
        rx.el.option("Hours", value="Hours"),
        rx.el.option("Days", value="Days"),
        value=AppState.ttl_unit,
        on_change=AppState.set_ttl_unit,
        class_name=(
            "bg-transparent text-white text-sm border-none outline-none cursor-pointer"
        ),
    )


def share() -> rx.Component:


    return page_shell(
        rx.el.div(
            rx.cond(
                AppState.share_url == "",
                # Input View
                rx.el.div(
                    rx.el.h1(
                        "Encrypt and Share",
                        class_name=(
                            "text-5xl font-extrabold tracking-tight text-center "
                            "bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent"
                        ),
                    ),
                    
                    # Textarea
                    rx.el.pre(
                        rx.el.div(
                            rx.el.div(
                                rx.foreach(
                                    AppState.line_numbers,
                                    lambda n: rx.el.span(n, class_name="block"),
                                ),
                                aria_hidden="true",
                                class_name="pr-4 font-mono border-r select-none border-zinc-300/5 text-zinc-700",
                            ),
                            rx.el.textarea(
                                placeholder="DATABASE_URL=postgres://...",
                                value=AppState.share_content,
                                on_change=AppState.set_share_content,
                                rows="6",
                                class_name=(
                                    "w-full p-0 text-base bg-transparent border-0 appearance-none resize-none "
                                    "hover:resize text-zinc-100 placeholder-zinc-500 focus:ring-0 focus:outline-none sm:text-sm font-mono"
                                ),
                            ),
                            class_name="flex items-start px-4 py-3 text-sm",
                        ),
                        class_name=(
                            "mt-8 w-full rounded border border-zinc-600 bg-transparent "
                            "focus-within:border-zinc-100/80 transition-all duration-150"
                        ),
                    ),

                    # Controls row
                    rx.el.div(
                        # Upload button
                        rx.el.div(
                            rx.upload(
                                rx.el.label(
                                    "Upload a file",
                                    html_for="file_input",
                                    class_name=(
                                        "flex items-center justify-center h-full w-full text-sm "
                                        "text-zinc-100 cursor-pointer"
                                    ),
                                ),
                                id="file_input",
                                on_drop=AppState.handle_file_upload(rx.upload_files(upload_id="file_input")),
                                no_click=False,
                                multiple=False,
                                border="none",
                                padding="0",
                                class_name="h-full w-full bg-transparent overflow-hidden",
                            ),
                            class_name=(
                                "w-full sm:w-1/5 h-16 border rounded border-zinc-600 "
                                "hover:border-zinc-100/80 duration-150 transition-all"
                            ),
                        ),

                        # Reads
                        rx.el.div(
                            rx.el.span("READS", class_name="block text-xs font-medium text-zinc-100"),
                            rx.el.input(
                                type="number",
                                value=AppState.reads,
                                on_change=AppState.set_reads,
                                min="0",
                                class_name=(
                                    "w-full p-0 text-base bg-transparent border-0 appearance-none "
                                    "text-zinc-100 placeholder-zinc-500 focus:ring-0 focus:outline-none sm:text-sm "
                                    "[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                ),
                            ),
                            class_name=(
                                "w-full h-16 px-3 py-2 duration-150 border rounded sm:w-2/5 "
                                "border-zinc-600 hover:border-zinc-100/80 focus-within:border-zinc-100/80"
                            ),
                        ),
                        # TTL
                        rx.el.div(
                            rx.el.span("TTL", class_name="block text-xs font-medium text-zinc-100"),
                            rx.el.div(
                                rx.el.input(
                                    type="number",
                                    value=AppState.ttl_value,
                                    on_change=AppState.set_ttl_value,
                                    min="0",
                                    class_name=(
                                        "w-full p-0 text-base bg-transparent border-0 appearance-none "
                                        "text-zinc-100 placeholder-zinc-500 focus:ring-0 focus:outline-none sm:text-sm "
                                        "[appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                    ),
                                ),
                                rx.el.div(
                                    _ttl_select(),
                                    class_name="absolute inset-y-0 right-0 flex items-center",
                                ),
                                class_name="relative",
                            ),
                            class_name=(
                                "relative w-full h-16 px-3 py-2 duration-150 border rounded sm:w-2/5 "
                                "border-zinc-600 hover:border-zinc-100/80 focus-within:border-zinc-100/80"
                            ),
                        ),
                        class_name="mt-4 flex flex-col sm:flex-row items-center justify-center w-full gap-4",
                    ),


                    # Share button
                    rx.el.button(
                        rx.cond(
                            AppState.share_loading, 
                            rx.icon(tag="settings", class_name="animate-spin text-zinc-900"),
                            "Share"
                        ),
                        on_click=AppState.do_share,
                        disabled=AppState.share_loading | (AppState.share_content == ""),
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
                        AppState.share_error != "",
                        rx.el.p(
                            AppState.share_error,
                            class_name="mt-3 text-sm text-red-400",
                        ),
                        rx.fragment(),
                    ),

                    # Helper text
                    rx.el.div(
                        rx.el.ul(
                            rx.el.li(
                                rx.el.p(
                                    rx.el.span("Reads:", class_name="font-semibold text-zinc-400"),
                                    " The number of reads determines how often the data can be shared, "
                                    "before it deletes itself. 0 means unlimited.",
                                ),
                            ),
                            rx.el.li(
                                rx.el.p(
                                    rx.el.span("TTL:", class_name="font-semibold text-zinc-400"),
                                    " You can add a TTL (time to live) to the data, to automatically delete "
                                    "it after a certain amount of time. 0 means no TTL.",
                                ),
                            ),
                            rx.el.p(
                                "Clicking Share will generate a new symmetrical key and encrypt your data before sending only the encrypted data to the server.",
                                class_name="mt-2",
                            ),
                            class_name="space-y-1 text-xs text-zinc-500 text-left",
                        ),
                        class_name="mt-8 flex flex-col items-start w-full",
                    ),



                    class_name="flex-1 flex flex-col items-center justify-center w-full max-w-3xl",
                ),
                # Success View
                rx.el.div(
                    rx.el.h1(
                        "Share this link with others",
                        class_name=(
                            "text-5xl font-extrabold tracking-tight text-center "
                            "bg-gradient-to-b from-white to-zinc-500 bg-clip-text text-transparent"
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.input(
                                value=AppState.share_url,
                                read_only=True,
                                class_name=(
                                    "w-full bg-transparent border-0 text-zinc-300 focus:ring-0 "
                                    "focus:outline-none sm:text-sm font-mono px-4"
                                ),
                            ),
                            rx.el.button(
                                rx.cond(
                                    AppState.share_copied,
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
                                on_click=AppState.copy_share_url,
                                class_name=(
                                    "h-full px-6 py-2 bg-white text-zinc-900 font-bold "
                                    "hover:bg-zinc-200 transition-colors border-l border-zinc-700 flex items-center"
                                ),
                            ),


                            class_name="flex items-center h-12 w-full",
                        ),
                        class_name=(
                            "mt-12 w-full max-w-3xl rounded border border-zinc-700 bg-transparent "
                            "overflow-hidden flex items-center"
                        ),
                    ),
                    rx.el.button(
                        "Share another",
                        on_click=AppState.reset_share,
                        class_name="mt-8 text-sm text-zinc-400 hover:text-white transition-colors",
                    ),
                    class_name="flex-1 flex flex-col items-center justify-center w-full",
                ),
            ),
            class_name="w-full flex flex-col items-center py-20 px-6",
        )
    )