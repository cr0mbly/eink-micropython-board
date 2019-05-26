from app.display import EinkDisplay
from app.display import StatusBar


def main():
    display = EinkDisplay().initialize_display()
    status_bar = StatusBar(display)
    status_bar.redraw_status_bar()


if __name__ == '__main__':
    main()
