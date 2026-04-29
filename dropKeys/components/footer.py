import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.p(
            "Built with ",
            rx.el.a(
                "Reflex",
                href="https://reflex.dev",
                target="_blank",
                class_name="text-zinc-300 hover:text-white underline underline-offset-2",
            ),
            class_name="text-xs text-zinc-600",
        ),

        class_name="w-full py-8 flex justify-center border-t border-zinc-900 bg-[#0d0d0d]",
    )