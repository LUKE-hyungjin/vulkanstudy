import reflex as rx
from rxconfig import config


# State 클래스 추가
class SidebarState(rx.State):
    # 각 사이드바 아이템의 열림/닫힘 상태를 저장
    is_projects_open: bool = False
    is_analytics_open: bool = False

    def toggle_projects(self):
        self.is_projects_open = not self.is_projects_open

    def toggle_analytics(self):
        self.is_analytics_open = not self.is_analytics_open


def sub_sidebar_item(text: str, href: str) -> rx.Component:
    return rx.link(
        rx.text(
            text,
            size="3",
            padding_left="2rem",
            padding_y="0.5rem",
            width="100%",
            style={
                "_hover": {
                    "color": rx.color("accent", 11),
                },
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_item(
    text: str,
    icon: str,
    href: str,
    sub_items: list = None,
    is_open: bool = False,
    on_toggle=None,
) -> rx.Component:
    chevron_icon = rx.cond(
        is_open, rx.icon(tag="chevron-down"), rx.icon(tag="chevron-right")
    )

    return rx.vstack(
        rx.hstack(
            rx.icon(tag=icon),
            rx.text(text, size="4"),
            rx.spacer(),
            rx.cond(
                sub_items is not None,
                chevron_icon,
            ),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
                "cursor": "pointer" if sub_items else "default",
            },
            on_click=on_toggle if sub_items else None,
        ),
        rx.cond(
            (sub_items is not None) & is_open,
            rx.vstack(
                *[
                    sub_sidebar_item(item["text"], item["href"])
                    for item in (sub_items or [])
                ],
                padding_top="0.5rem",
                width="100%",
            ),
        ),
        align_items="flex-start",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item(
            "Projects",
            "square-library",
            "/#",
            sub_items=[
                {"text": "Active Projects", "href": "/#active"},
                {"text": "Archived", "href": "/#archived"},
                {"text": "Templates", "href": "/#templates"},
            ],
            is_open=SidebarState.is_projects_open,
            on_toggle=SidebarState.toggle_projects,
        ),
        sidebar_item(
            "Analytics",
            "bar-chart-4",
            "/#",
            sub_items=[
                {"text": "Overview", "href": "/#overview"},
                {"text": "Reports", "href": "/#reports"},
            ],
            is_open=SidebarState.is_analytics_open,
            on_toggle=SidebarState.toggle_analytics,
        ),
        sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )


def index() -> rx.Component:
    return rx.container(
        rx.hstack(
            sidebar_items(),
            rx.logo(),
        ),
    )
