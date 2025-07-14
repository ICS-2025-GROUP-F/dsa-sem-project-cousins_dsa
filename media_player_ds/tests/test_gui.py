import tkinter as tk


def test_gui():
    root = tk.Tk()
    root.title("Test GUI")
    root.geometry("300x200")

    label = tk.Label(root, text="If you see this, Tkinter works!", font=("Arial", 12))
    label.pack(pady=50)

    button = tk.Button(root, text="Close", command=root.quit)
    button.pack()

    print("Test GUI should be visible now...")
    root.mainloop()
    print("Test GUI closed.")


if __name__ == "__main__":
    test_gui()