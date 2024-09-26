import tkinter as tk
from tkinter import ttk


class MultiSelectDropdown(tk.Frame):
    """
    A Tkinter Frame widget that provides a multi-select dropdown functionality.

    This class simulates a dropdown using a Toplevel window and a Listbox, allowing
    users to select multiple options from a list. The selected options are displayed
    on the main frame.

    :param master: The parent widget.
    :type master: tk.Widget
    :param options: A list of available options to choose from.
    :type options: list[str]
    :param selected_options: A list to store the options selected by the user.
    :type selected_options: list[str]
    :param args: Additional positional arguments for the parent `tk.Frame`.
    :param kwargs: Additional keyword arguments for the parent `tk.Frame`.
    """
    def __init__(self, master, options: list[str], selected_options: list[str], *args, **kwargs):
        super().__init__(master, *args, **kwargs)  # Initialize the Frame
        self.listbox = None
        self.dropdown_window = None
        self.options = options
        self.selected_options = selected_options

        # Create a button to open the dropdown
        self.button = ttk.Button(self, text="Select Options to Remove", command=self.show_dropdown)
        self.button.pack(pady=10)

        # Label to show selected items
        self.label = ttk.Label(self, text="Selected: None")
        self.label.pack(pady=10)

    def show_dropdown(self):
        """
        Displays a dropdown window with a list of options for the user to select.

        This method creates a Toplevel window containing a Listbox with multiple
        selection mode enabled. It allows the user to select options from the list of
        available options.

        :return: None
        """
        # Create a Toplevel window to simulate a dropdown
        self.dropdown_window = tk.Toplevel(self)
        self.dropdown_window.geometry("500x350")
        self.dropdown_window.grab_set()

        self.listbox = tk.Listbox(self.dropdown_window, selectmode=tk.MULTIPLE)
        self.listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        for option in self.options:
            self.listbox.insert(tk.END, option)

        confirm_button = ttk.Button(self.dropdown_window, text=f"Remove Courses", command=self.confirm_selection)
        confirm_button.pack(pady=5)

    def confirm_selection(self) -> None:
        """
        Confirms the user's selection from the dropdown.

        Retrieves the indices of the selected options from the Listbox, updates the
        `selected_options` list, and displays the selected options in the label on the
        main frame.

        :return: None
        """
        selected_indices = self.listbox.curselection()
        self.selected_options.extend([self.options[i] for i in selected_indices])

        selected_text = ", ".join(self.selected_options) if self.selected_options else "None"
        self.label.config(text=f"Selected: {selected_text}")

        self.dropdown_window.destroy()
