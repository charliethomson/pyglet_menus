
from menu import Menu, Button
import logging


def main():
    logger = logging.Logger("MainLogger")
    logging.basicConfig(filename="./logs/test.log")
    menu = Menu("Main menu", logger=logger)

    menu.add_element(Button(500, 500, 200, 400, "Test Button", "A TEST"))

if __name__ == "__main__":
    main()