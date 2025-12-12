from tkinter import Tk
from app.ui.main_app import eCommerce

def main():
    """Main entry point for the eCommerce Order Manager application"""
    root = Tk()
    app = eCommerce(root)
    root.mainloop()

if __name__ == "__main__":
    main()