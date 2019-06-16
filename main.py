from app.display import EinkDisplay, StatusBar, AppDrawer


def main():
    display = EinkDisplay()
    display.initialize_display()

    status_bar = StatusBar(display)
    status_bar.set_notification('Hi There')
    status_bar.redraw_status_bar()

    app_drawer = AppDrawer(display)
    app_drawer.load_apps_for_display()
    app_drawer.select_app(1)
    app_drawer.redraw_app_drawer()


if __name__ == '__main__':
    main()
