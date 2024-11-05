"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from .pages.index import index


app = rx.App()
app.add_page(index)
