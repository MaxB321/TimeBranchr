from dotenv import load_dotenv
import gui.main_window


if __name__ == "__main__":
    load_dotenv()
    gui.main_window.display_window()
    