import reflex as rx
from reflex_google_auth import google_oauth_provider, handle_google_login
from ..state import AppState
from ..config import settings


def _google_button() -> rx.Component:
    return google_oauth_provider(
        rx.el.button(
            rx.el.span(
                rx.html(
                    '<svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg">'
                    '<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>'
                    '<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>'
                    '<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>'
                    '<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>'
                    "</svg>"
                ),
                class_name="flex-shrink-0",
            ),
            "Continue with Google",
            on_click=handle_google_login(
                on_success=AppState.on_login_success,
            ),

            class_name=(
                "sm:w-full sm:text-center inline-flex items-center justify-center gap-3 "
                "rounded px-4 py-1.5 md:py-2 text-base font-semibold leading-7 text-white "
                "ring-1 ring-zinc-600 hover:bg-white hover:text-zinc-900 duration-150 "
                "hover:ring-white transition-all cursor-pointer disabled:opacity-50 "
                "disabled:cursor-not-allowed"
            ),

        ),
        client_id=settings.google_client_id,
    )


def loading_overlay() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white mb-4 mx-auto"
            ),
            rx.el.p("Securing session...", class_name="text-white text-xl font-medium tracking-tight"),
            rx.el.p("Connecting to vault", class_name="text-zinc-500 text-sm mt-2"),
            class_name="text-center p-8 rounded-2xl bg-zinc-900/50 backdrop-blur-xl border border-white/10 shadow-2xl",
        ),
        class_name="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-md transition-all duration-300",
    )


def auth_callback() -> rx.Component:

    return rx.el.div(
        rx.el.div(
            rx.el.h1("Authenticating...", class_name="text-2xl font-bold mb-4"),
            rx.el.div(class_name="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto"),
            class_name="text-center",
        ),
        class_name="min-h-screen flex items-center justify-center bg-[#0e0e0e] text-white",
        on_mount=rx.redirect("/"),
    )


def login() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AppState.is_authenticating,
            loading_overlay(),
            rx.fragment(),
        ),
        rx.el.main(

            rx.el.div(
                rx.el.h1(
                    rx.el.span("Drop", class_name="text-white"),
                    rx.el.span("Keys", class_name="text-zinc-500"),
                    class_name="text-6xl sm:text-7xl md:text-8xl font-bold tracking-tighter mb-8",
                ),
                rx.el.h2(
                    "Share Environment",
                    rx.el.br(),
                    "Variables Securely",
                    class_name="py-4 text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-center text-transparent bg-gradient-to-t bg-clip-text from-zinc-100/50 to-white",
                ),
                rx.el.p(
                    "Your document is encrypted in your browser before being stored for a limited period of time and read operations. Unencrypted data never leaves your browser.",
                    class_name="mt-6 leading-5 text-zinc-600 sm:text-center",
                ),
                rx.el.div(
                    _google_button(),
                    class_name="flex flex-col justify-center gap-4 mx-auto mt-8 w-full max-w-lg"
                ),
                class_name="flex flex-col items-center justify-center max-w-3xl px-8 mx-auto mt-8 sm:min-h-screen sm:mt-0 sm:px-0",
            ),
        ),
        class_name="min-h-screen flex flex-col bg-[#0e0e0e] text-white font-sans",
    )