from app.display import EinkDisplay


def main():
    display = EinkDisplay()
    display.render_window(100, 100, 150, 130)


if __name__ == '__main__':
    main()
