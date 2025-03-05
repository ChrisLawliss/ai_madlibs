import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re
import sys

class MadLibsCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mad Libs Creator")
        self.root.geometry("800x600")
        
        # Data structures
        self.current_madlib = {
            "title": "",
            "template": "",
            "placeholders": []
        }
        self.saved_madlibs = []
        self.current_file = None
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tab = ttk.Frame(self.notebook)
        self.play_tab = ttk.Frame(self.notebook)
        self.manage_tab = ttk.Frame(self.notebook)
        self.ai_tab = ttk.Frame(self.notebook)  # New AI tab
        
        self.notebook.add(self.create_tab, text="Create")
        self.notebook.add(self.play_tab, text="Play")
        self.notebook.add(self.manage_tab, text="Manage")
        self.notebook.add(self.ai_tab, text="AI Generator")  # Add AI tab
        
        # Setup each tab
        self.setup_create_tab()
        self.setup_play_tab()
        self.setup_manage_tab()
        self.setup_ai_tab()  # Setup AI tab
        
        # Create menu
        self.create_menu()
        
        # Load saved mad libs if available
        self.load_madlibs()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_madlib)
        file_menu.add_command(label="Open", command=self.open_madlibs)
        file_menu.add_command(label="Save", command=self.save_madlibs)
        file_menu.add_command(label="Save As", command=self.save_as_madlibs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Templates menu
        templates_menu = tk.Menu(menubar, tearoff=0)
        templates_menu.add_command(label="Load Template", command=self.load_template)
        
        menubar.add_cascade(label="Templates", menu=templates_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
        
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def setup_create_tab(self):
        # Title frame
        title_frame = ttk.LabelFrame(self.create_tab, text="Mad Lib Title")
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.title_entry = ttk.Entry(title_frame, width=50)
        self.title_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Template frame
        template_frame = ttk.LabelFrame(self.create_tab, text="Template")
        template_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        template_instructions = ttk.Label(template_frame, 
                                         text="Write your story and use [noun], [verb], etc. for placeholders.")
        template_instructions.pack(anchor=tk.W, padx=5, pady=2)
        
        self.template_text = tk.Text(template_frame, wrap=tk.WORD)
        self.template_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.create_tab)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        extract_btn = ttk.Button(buttons_frame, text="Extract Placeholders", command=self.extract_placeholders)
        extract_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        save_btn = ttk.Button(buttons_frame, text="Save Mad Lib", command=self.save_current_madlib)
        save_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Placeholders frame
        self.placeholders_frame = ttk.LabelFrame(self.create_tab, text="Placeholders")
        self.placeholders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.placeholders_list = tk.Listbox(self.placeholders_frame)
        self.placeholders_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def setup_play_tab(self):
        # Selection frame
        selection_frame = ttk.Frame(self.play_tab)
        selection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(selection_frame, text="Select a Mad Lib:").pack(side=tk.LEFT, padx=5, pady=5)
        
        self.madlib_selector = ttk.Combobox(selection_frame, state="readonly")
        self.madlib_selector.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.madlib_selector.bind("<<ComboboxSelected>>", self.load_selected_madlib)
        
        # Add a button to load example templates
        example_btn = ttk.Button(selection_frame, text="Try Examples", command=self.load_example_templates)
        example_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Inputs frame
        self.inputs_frame = ttk.LabelFrame(self.play_tab, text="Fill in the blanks")
        self.inputs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(self.play_tab, text="Your Mad Lib Story")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(self.results_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Generate button
        generate_btn = ttk.Button(self.play_tab, text="Generate Story", command=self.generate_story)
        generate_btn.pack(padx=10, pady=10)
    
    def setup_manage_tab(self):
        # List frame
        list_frame = ttk.LabelFrame(self.manage_tab, text="Your Mad Libs")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.madlibs_listbox = tk.Listbox(list_frame)
        self.madlibs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.madlibs_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.madlibs_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.manage_tab)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        edit_btn = ttk.Button(buttons_frame, text="Edit", command=self.edit_madlib)
        edit_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        delete_btn = ttk.Button(buttons_frame, text="Delete", command=self.delete_madlib)
        delete_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def setup_ai_tab(self):
        """Setup the AI Generator tab"""
        # API Key frame
        api_frame = ttk.LabelFrame(self.ai_tab, text="OpenAI API Key")
        api_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Try to load API key from environment variable
        if 'OPENAI_API_KEY' in os.environ:
            self.api_key_var.set(os.environ['OPENAI_API_KEY'])
        
        # Toggle button to show/hide API key
        self.show_key = tk.BooleanVar(value=False)
        show_key_check = ttk.Checkbutton(api_frame, text="Show", variable=self.show_key, 
                                         command=lambda: api_key_entry.config(show='' if self.show_key.get() else '*'))
        show_key_check.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Prompt frame
        prompt_frame = ttk.LabelFrame(self.ai_tab, text="Describe Your Mad Lib")
        prompt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        prompt_instructions = ttk.Label(prompt_frame, 
                                       text="Describe the theme or story for your Mad Lib. Be specific about the setting, characters, or situation.")
        prompt_instructions.pack(anchor=tk.W, padx=5, pady=2)
        
        self.prompt_text = tk.Text(prompt_frame, wrap=tk.WORD, height=5)
        self.prompt_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Example prompts
        examples_frame = ttk.LabelFrame(self.ai_tab, text="Example Prompts")
        examples_frame.pack(fill=tk.X, padx=10, pady=5)
        
        examples = [
            "Create a Mad Lib about a haunted house adventure with ghosts and secret passages.",
            "Make a funny Mad Lib about someone's first day at a new job.",
            "Write a Mad Lib about an alien visiting Earth for the first time.",
            "Create a Mad Lib about a cooking competition that goes hilariously wrong."
        ]
        
        for example in examples:
            example_btn = ttk.Button(examples_frame, text="Use", 
                                    command=lambda e=example: self.use_example_prompt(e))
            example_btn.pack(side=tk.LEFT, padx=5, pady=5)
            
            ttk.Label(examples_frame, text=example[:30] + "...").pack(side=tk.LEFT, padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.Frame(self.ai_tab)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="Complexity:").pack(side=tk.LEFT, padx=5, pady=5)
        
        self.complexity_var = tk.StringVar(value="Medium")
        complexity_combo = ttk.Combobox(options_frame, textvariable=self.complexity_var, 
                                       values=["Simple", "Medium", "Complex"], state="readonly", width=10)
        complexity_combo.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Style:").pack(side=tk.LEFT, padx=5, pady=5)
        
        self.style_var = tk.StringVar(value="Funny")
        style_combo = ttk.Combobox(options_frame, textvariable=self.style_var, 
                                  values=["Funny", "Serious", "Mysterious", "Educational", "Silly"], state="readonly", width=10)
        style_combo.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Generate button
        generate_frame = ttk.Frame(self.ai_tab)
        generate_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.generate_btn = ttk.Button(generate_frame, text="Generate Mad Lib Template", 
                                      command=self.generate_ai_template)
        self.generate_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.status_label = ttk.Label(generate_frame, text="")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.ai_tab, text="Generated Template")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.ai_tab)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.use_template_btn = ttk.Button(buttons_frame, text="Use This Template", 
                                          command=self.use_generated_template, state=tk.DISABLED)
        self.use_template_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def extract_placeholders(self):
        template = self.template_text.get("1.0", tk.END).strip()
        if not template:
            messagebox.showwarning("Warning", "Please enter a template first.")
            return
        
        # Find all placeholders in [brackets]
        placeholders = re.findall(r'\[(.*?)\]', template)
        
        # Remove duplicates but preserve order
        unique_placeholders = []
        for p in placeholders:
            if p not in unique_placeholders:
                unique_placeholders.append(p)
        
        # Update the current madlib
        self.current_madlib["template"] = template
        self.current_madlib["placeholders"] = unique_placeholders
        
        # Update the placeholders list
        self.placeholders_list.delete(0, tk.END)
        for p in unique_placeholders:
            self.placeholders_list.insert(tk.END, p)
        
        messagebox.showinfo("Success", f"Found {len(unique_placeholders)} unique placeholders.")
    
    def save_current_madlib(self):
        title = self.title_entry.get().strip()
        template = self.template_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a title.")
            return
        
        if not template:
            messagebox.showwarning("Warning", "Please enter a template.")
            return
        
        if not self.current_madlib["placeholders"]:
            messagebox.showwarning("Warning", "No placeholders found. Please extract placeholders first.")
            return
        
        # Update the current madlib
        self.current_madlib["title"] = title
        self.current_madlib["template"] = template
        
        # Check if we're editing an existing madlib
        existing_index = -1
        for i, madlib in enumerate(self.saved_madlibs):
            if madlib["title"] == title:
                existing_index = i
                break
        
        if existing_index >= 0:
            # Update existing
            self.saved_madlibs[existing_index] = self.current_madlib.copy()
            messagebox.showinfo("Success", f"Updated Mad Lib: {title}")
        else:
            # Add new
            self.saved_madlibs.append(self.current_madlib.copy())
            messagebox.showinfo("Success", f"Saved new Mad Lib: {title}")
        
        # Update UI
        self.update_madlibs_ui()
        
        # Auto-save
        self.save_madlibs()
    
    def update_madlibs_ui(self):
        # Update the listbox in manage tab
        self.madlibs_listbox.delete(0, tk.END)
        for madlib in self.saved_madlibs:
            self.madlibs_listbox.insert(tk.END, madlib["title"])
        
        # Update the combobox in play tab
        titles = [madlib["title"] for madlib in self.saved_madlibs]
        self.madlib_selector["values"] = titles
        if titles:
            self.madlib_selector.current(0)
    
    def load_selected_madlib(self, event=None):
        selected_title = self.madlib_selector.get()
        if not selected_title:
            return
        
        # Find the selected madlib
        selected_madlib = None
        for madlib in self.saved_madlibs:
            if madlib["title"] == selected_title:
                selected_madlib = madlib
                break
        
        if not selected_madlib:
            return
        
        # Clear previous inputs
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        
        # Create input fields for each placeholder
        self.placeholder_entries = {}
        for i, placeholder in enumerate(selected_madlib["placeholders"]):
            frame = ttk.Frame(self.inputs_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = ttk.Label(frame, text=f"{placeholder}:", width=20)
            label.pack(side=tk.LEFT, padx=5, pady=2)
            
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
            
            self.placeholder_entries[placeholder] = entry
    
    def generate_story(self):
        selected_title = self.madlib_selector.get()
        if not selected_title:
            messagebox.showwarning("Warning", "Please select a Mad Lib.")
            return
        
        # Find the selected madlib
        selected_madlib = None
        for madlib in self.saved_madlibs:
            if madlib["title"] == selected_title:
                selected_madlib = madlib
                break
        
        if not selected_madlib:
            return
        
        # Get user inputs
        inputs = {}
        for placeholder, entry in self.placeholder_entries.items():
            value = entry.get().strip()
            if not value:
                messagebox.showwarning("Warning", f"Please fill in the {placeholder} field.")
                return
            inputs[placeholder] = value
        
        # Generate the story
        story = selected_madlib["template"]
        for placeholder, value in inputs.items():
            story = story.replace(f"[{placeholder}]", value)
        
        # Display the result
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", story)
        self.result_text.config(state=tk.DISABLED)
    
    def edit_madlib(self):
        selected_index = self.madlibs_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a Mad Lib to edit.")
            return
        
        selected_madlib = self.saved_madlibs[selected_index[0]]
        
        # Load the selected madlib into the create tab
        self.current_madlib = selected_madlib.copy()
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, selected_madlib["title"])
        
        self.template_text.delete("1.0", tk.END)
        self.template_text.insert("1.0", selected_madlib["template"])
        
        self.placeholders_list.delete(0, tk.END)
        for p in selected_madlib["placeholders"]:
            self.placeholders_list.insert(tk.END, p)
        
        # Switch to create tab
        self.notebook.select(0)
    
    def delete_madlib(self):
        selected_index = self.madlibs_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a Mad Lib to delete.")
            return
        
        selected_title = self.saved_madlibs[selected_index[0]]["title"]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", 
                                      f"Are you sure you want to delete '{selected_title}'?")
        if not confirm:
            return
        
        # Delete the madlib
        del self.saved_madlibs[selected_index[0]]
        
        # Update UI
        self.update_madlibs_ui()
        
        # Auto-save
        self.save_madlibs()
        
        messagebox.showinfo("Success", f"Deleted Mad Lib: {selected_title}")
    
    def new_madlib(self):
        # Clear current madlib
        self.current_madlib = {
            "title": "",
            "template": "",
            "placeholders": []
        }
        
        self.title_entry.delete(0, tk.END)
        self.template_text.delete("1.0", tk.END)
        self.placeholders_list.delete(0, tk.END)
        
        # Switch to create tab
        self.notebook.select(0)
    
    def open_madlibs(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, "r") as file:
                self.saved_madlibs = json.load(file)
            
            self.current_file = filepath
            self.update_madlibs_ui()
            messagebox.showinfo("Success", f"Loaded Mad Libs from {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def save_madlibs(self):
        if not self.current_file:
            self.save_as_madlibs()
            return
        
        try:
            with open(self.current_file, "w") as file:
                json.dump(self.saved_madlibs, file, indent=2)
            messagebox.showinfo("Success", f"Saved Mad Libs to {self.current_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def save_as_madlibs(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        self.current_file = filepath
        self.save_madlibs()
    
    def load_madlibs(self):
        # Try to load from default location
        default_path = os.path.join(os.path.expanduser("~"), "madlibs.json")
        
        if os.path.exists(default_path):
            try:
                with open(default_path, "r") as file:
                    self.saved_madlibs = json.load(file)
                
                self.current_file = default_path
                self.update_madlibs_ui()
            except:
                # If loading fails, start with empty list
                self.saved_madlibs = []
        else:
            self.saved_madlibs = []
    
    def show_about(self):
        messagebox.showinfo("About", "Mad Libs Creator\nVersion 1.0\n\nCreate and play your own Mad Libs games!")
    
    def show_help(self):
        help_text = """
        Mad Libs Creator Help
        
        Create Tab:
        1. Enter a title for your Mad Lib
        2. Write your template using [noun], [verb], etc. for placeholders
        3. Click 'Extract Placeholders' to find all placeholders
        4. Click 'Save Mad Lib' to save your creation
        
        Play Tab:
        1. Select a Mad Lib from the dropdown
        2. Fill in all the requested words
        3. Click 'Generate Story' to see your completed Mad Lib
        
        Manage Tab:
        1. View all your saved Mad Libs
        2. Select one to edit or delete
        """
        messagebox.showinfo("Help", help_text)

    def load_template(self):
        # Check if templates directory exists
        templates_dir = "templates"
        if not os.path.exists(templates_dir):
            messagebox.showwarning("Warning", "Templates directory not found.")
            return
        
        # Get list of template files
        template_files = [f for f in os.listdir(templates_dir) if f.endswith('.json')]
        
        if not template_files:
            messagebox.showwarning("Warning", "No template files found in templates directory.")
            return
        
        # Create a simple dialog to select a template
        template_dialog = tk.Toplevel(self.root)
        template_dialog.title("Select a Template")
        template_dialog.geometry("300x300")
        template_dialog.transient(self.root)
        template_dialog.grab_set()
        
        ttk.Label(template_dialog, text="Choose a template:").pack(pady=10)
        
        # Create a listbox with templates
        template_listbox = tk.Listbox(template_dialog)
        template_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add template names to listbox (without .json extension)
        for template_file in template_files:
            template_name = os.path.splitext(template_file)[0].replace('_', ' ').title()
            template_listbox.insert(tk.END, template_name)
        
        def select_template():
            selection = template_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a template.")
                return
            
            selected_file = template_files[selection[0]]
            template_path = os.path.join(templates_dir, selected_file)
            
            try:
                with open(template_path, 'r') as file:
                    template_data = json.load(file)
                    
                    # Load the template into the current madlib
                    self.current_madlib = template_data.copy()
                    
                    # Update UI
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, template_data["title"])
                    
                    self.template_text.delete("1.0", tk.END)
                    self.template_text.insert("1.0", template_data["template"])
                    
                    self.placeholders_list.delete(0, tk.END)
                    for p in template_data["placeholders"]:
                        self.placeholders_list.insert(tk.END, p)
                    
                    # Switch to create tab
                    self.notebook.select(0)
                    
                    messagebox.showinfo("Success", f"Loaded template: {template_data['title']}")
                    template_dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {str(e)}")
        
        # Add buttons
        button_frame = ttk.Frame(template_dialog)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Select", command=select_template).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=template_dialog.destroy).pack(side=tk.RIGHT, padx=10)

    def load_example_templates(self):
        # Check if templates directory exists
        templates_dir = "templates"
        if not os.path.exists(templates_dir):
            # Try to create templates on the fly
            try:
                self.create_example_templates()
            except Exception as e:
                messagebox.showerror("Error", f"Could not create example templates: {str(e)}")
                return
        
        # Get list of template files
        template_files = [f for f in os.listdir(templates_dir) if f.endswith('.json')]
        
        if not template_files:
            messagebox.showwarning("Warning", "No template files found in templates directory.")
            return
        
        # Create a simple dialog to select a template
        template_dialog = tk.Toplevel(self.root)
        template_dialog.title("Example Templates")
        template_dialog.geometry("400x400")
        template_dialog.transient(self.root)
        template_dialog.grab_set()
        
        ttk.Label(template_dialog, text="Choose an example template to play:").pack(pady=10)
        
        # Create a listbox with templates
        template_listbox = tk.Listbox(template_dialog, font=("Arial", 11))
        template_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add template names to listbox (without .json extension)
        for template_file in template_files:
            template_name = os.path.splitext(template_file)[0].replace('_', ' ').title()
            template_listbox.insert(tk.END, template_name)
        
        # Add a description label
        description_label = ttk.Label(template_dialog, text="", wraplength=380)
        description_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Show description when template is selected
        def show_description(event):
            selection = template_listbox.curselection()
            if not selection:
                return
            
            selected_file = template_files[selection[0]]
            template_path = os.path.join(templates_dir, selected_file)
            
            try:
                with open(template_path, 'r') as file:
                    template_data = json.load(file)
                    # Show a preview of the template
                    preview = template_data["template"]
                    if len(preview) > 150:
                        preview = preview[:150] + "..."
                    description_label.config(text=f"Preview: {preview}")
            except Exception:
                description_label.config(text="Could not load template preview.")
        
        template_listbox.bind("<<ListboxSelect>>", show_description)
        
        def select_template():
            selection = template_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a template.")
                return
            
            selected_file = template_files[selection[0]]
            template_path = os.path.join(templates_dir, selected_file)
            
            try:
                with open(template_path, 'r') as file:
                    template_data = json.load(file)
                    
                # Add this template to saved madlibs if not already there
                template_exists = False
                for madlib in self.saved_madlibs:
                    if madlib["title"] == template_data["title"]:
                        template_exists = True
                        break
                
                if not template_exists:
                    self.saved_madlibs.append(template_data.copy())
                    self.update_madlibs_ui()
                
                # Select this template in the play tab
                index = self.madlib_selector["values"].index(template_data["title"]) if template_data["title"] in self.madlib_selector["values"] else 0
                self.madlib_selector.current(index)
                self.load_selected_madlib()
                
                template_dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load template: {str(e)}")
        
        # Add buttons
        button_frame = ttk.Frame(template_dialog)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Play This Template", command=select_template).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=template_dialog.destroy).pack(side=tk.RIGHT, padx=10)

    def create_example_templates(self):
        """Create example templates if they don't exist"""
        templates_dir = "templates"
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        # Define the example templates
        templates = [
            # Original 5 templates
            {
                "filename": "space_adventure.json",
                "data": {
                    "title": "Space Adventure",
                    "template": "Captain [name] embarked on a journey to the [adjective] planet [planet_name]. The ship's [noun] malfunctioned as they [verb_past] through an asteroid field. \"[exclamation]!\" shouted the captain, \"We need to [verb] immediately!\" The alien crew members began to [verb] frantically. Eventually, they landed on a [adjective] moon where [plural_noun] roamed freely. It was the most [adjective] adventure in the history of space exploration.",
                    "placeholders": ["name", "adjective", "planet_name", "noun", "verb_past", "exclamation", "verb", "verb", "adjective", "plural_noun", "adjective"]
                }
            },
            {
                "filename": "fairy_tale.json",
                "data": {
                    "title": "Once Upon a Time",
                    "template": "Once upon a time, in a [adjective] kingdom, there lived a [noun] named [name]. Every day, they would [verb] by the [adjective] [place]. One day, a [adjective] [magical_creature] appeared and granted them three [plural_noun]. \"[exclamation]!\" they shouted with joy. With their new [plural_noun], [name] decided to [verb] the evil [villain]. After a [adjective] battle, they lived [adverb] ever after.",
                    "placeholders": ["adjective", "noun", "name", "verb", "adjective", "place", "adjective", "magical_creature", "plural_noun", "exclamation", "plural_noun", "name", "verb", "villain", "adjective", "adverb"]
                }
            },
            {
                "filename": "cooking_disaster.json",
                "data": {
                    "title": "Kitchen Catastrophe",
                    "template": "Today I decided to cook a [adjective] meal for my [relative]. I started by [verb_ending_in_ing] [number] [plural_food] in a [adjective] pan. I accidentally added too much [substance], which made everything smell like [smelly_item]. \"[exclamation]!\" I shouted as the mixture began to [verb]. I tried to fix it by adding a [adjective] [food_item], but that only made it [verb]. In the end, we just ordered [type_of_cuisine] food and [verb_past] while watching [TV_show].",
                    "placeholders": ["adjective", "relative", "verb_ending_in_ing", "number", "plural_food", "adjective", "substance", "smelly_item", "exclamation", "verb", "adjective", "food_item", "verb", "type_of_cuisine", "verb_past", "TV_show"]
                }
            },
            {
                "filename": "superhero_origin.json",
                "data": {
                    "title": "Birth of a Hero",
                    "template": "By day, [name] was just an ordinary [occupation], but at night, they became [superhero_name], the most [adjective] superhero in [city_name]! Their superpowers included [verb_ending_in_ing] [adverb] and shooting [plural_noun] from their [body_part]. Their arch-nemesis, [villain_name], was always plotting to [verb] the city's supply of [plural_noun]. With the help of their sidekick, [animal], [superhero_name] always saved the day by using their [adjective] [noun] to [verb] the day!",
                    "placeholders": ["name", "occupation", "superhero_name", "adjective", "city_name", "verb_ending_in_ing", "adverb", "plural_noun", "body_part", "villain_name", "verb", "plural_noun", "animal", "superhero_name", "adjective", "noun", "verb"]
                }
            },
            {
                "filename": "vacation_disaster.json",
                "data": {
                    "title": "Vacation Disaster",
                    "template": "Last summer, my family decided to go on a [adjective] vacation to [place]. We packed our [plural_noun] and headed off in our [adjective] [vehicle]. After [number] hours of traveling, we realized we had forgotten our [important_item]! \"[exclamation]!\" my [family_member] screamed. We stopped at a [adjective] store to buy a new one, but they only had [adjective] ones. The hotel was even worse! The room was full of [plural_noun] and the [room_item] was [verb_ending_in_ing]. We ended up [verb_ending_in_ing] at a nearby [place] instead, which turned out to be the most [adjective] part of our trip.",
                    "placeholders": ["adjective", "place", "plural_noun", "adjective", "vehicle", "number", "important_item", "exclamation", "family_member", "adjective", "adjective", "plural_noun", "room_item", "verb_ending_in_ing", "verb_ending_in_ing", "place", "adjective"]
                }
            },
            
            # 10 new templates
            {
                "filename": "haunted_house.json",
                "data": {
                    "title": "The Haunted House",
                    "template": "Last night, I decided to explore the [adjective] haunted house on [street_name] Street. I brought my trusty [noun] for protection. As I approached the [adjective] door, I heard a [sound] coming from inside. \"[exclamation]!\" I whispered. I slowly turned the [adjective] doorknob and entered. The floor was covered in [plural_noun] and the walls were dripping with [substance]. Suddenly, a [adjective] [monster] jumped out and started [verb_ending_in_ing] around the room. I tried to [verb], but my legs wouldn't move. The ghost whispered, \"[silly_phrase]\" and then disappeared in a puff of [color] smoke. I'll never go [verb_ending_in_ing] in a haunted house again!",
                    "placeholders": ["adjective", "street_name", "noun", "adjective", "sound", "exclamation", "adjective", "plural_noun", "substance", "adjective", "monster", "verb_ending_in_ing", "verb", "silly_phrase", "color", "verb_ending_in_ing"]
                }
            },
            {
                "filename": "job_interview.json",
                "data": {
                    "title": "My Disastrous Job Interview",
                    "template": "I was so [adjective] about my job interview at [company_name]. I put on my most [adjective] [clothing_item] and practiced answering questions in front of my [noun]. When I arrived, the receptionist asked me to [verb] in the waiting room. After [number] minutes, a [adjective] person named [name] called me into their office. The interview started well until they asked me why I wanted to [verb] for their company. I accidentally said, \"Because I'm really good at [verb_ending_in_ing] [plural_noun]!\" The interviewer looked [adjective] and then asked about my greatest weakness. I blurted out, \"[food]!\" Before I knew it, I was [verb_ending_in_ing] out the door. I guess I won't be [verb_ending_in_ing] there anytime soon!",
                    "placeholders": ["adjective", "company_name", "adjective", "clothing_item", "noun", "verb", "number", "adjective", "name", "verb", "verb_ending_in_ing", "plural_noun", "adjective", "food", "verb_ending_in_ing", "verb_ending_in_ing"]
                }
            },
            {
                "filename": "alien_encounter.json",
                "data": {
                    "title": "Close Encounter",
                    "template": "I was [verb_ending_in_ing] in my backyard when a [adjective] light appeared in the sky. A [color] spacecraft landed on my [noun]. The door opened with a [sound], and [number] aliens with [body_part_plural] on their heads stepped out. \"[greeting]!\" their leader said in a [adjective] voice. \"We come from the planet [made_up_word] and need your [plural_noun] to save our civilization!\" I was so [emotion] that I could only [verb]. They offered me a [adjective] [food] as a gift. Before leaving, they [adverb] promised to return next [day_of_week]. Now I keep a [noun] ready just in case they come back for more [plural_noun].",
                    "placeholders": ["verb_ending_in_ing", "adjective", "color", "noun", "sound", "number", "body_part_plural", "greeting", "adjective", "made_up_word", "plural_noun", "emotion", "verb", "adjective", "food", "adverb", "day_of_week", "noun", "plural_noun"]
                }
            },
            {
                "filename": "first_date.json",
                "data": {
                    "title": "First Date Fiasco",
                    "template": "I was so [adjective] about my first date with [name]. I decided to wear my favorite [color] [clothing_item] and meet them at a [adjective] restaurant called [restaurant_name]. When I arrived, I accidentally tripped over a [noun] and [verb_past] right into the [noun]. [name] was already sitting at our table, looking [adjective] in their [clothing_item]. I tried to act [adverb], but when I went to [verb] my chair, I [verb_past] instead. The waiter came over and I nervously ordered [food] with extra [food_ingredient]. During our conversation, I mentioned my love for [verb_ending_in_ing] [plural_noun], which made [name] look at me [adverb]. By the end of the night, I had [verb_past] my [body_part] and spilled [beverage] all over the table. Surprisingly, [name] still wants to [verb] again next [day_of_week]!",
                    "placeholders": ["adjective", "name", "color", "clothing_item", "adjective", "restaurant_name", "noun", "verb_past", "noun", "name", "adjective", "clothing_item", "adverb", "verb", "verb_past", "food", "food_ingredient", "verb_ending_in_ing", "plural_noun", "name", "adverb", "verb_past", "body_part", "beverage", "name", "verb", "day_of_week"]
                }
            },
            {
                "filename": "sports_commentary.json",
                "data": {
                    "title": "Sports Commentary",
                    "template": "Welcome to the championship [sport] game between the [city] [plural_animal] and the [city] [plural_noun]! The [plural_animal]'s star player, [name], is known for their ability to [verb] [adverb]. The crowd is [verb_ending_in_ing] as the game begins! Oh my! [name] just [verb_past] the [noun] across the entire [place]! The coach is [verb_ending_in_ing] on the sidelines. Wait - a [adjective] [animal] has run onto the field! Security is trying to [verb] it, but it's too [adjective]! Meanwhile, the [plural_noun] are attempting their famous \"[silly_phrase]\" play. The referee throws a [color] flag and calls a penalty for illegal [verb_ending_in_ing]. With only [number] seconds left, [name] makes the winning move by [verb_ending_in_ing] over three defenders! The [plural_animal] win the [adjective] trophy, and the celebration is absolutely [adjective]!",
                    "placeholders": ["sport", "city", "plural_animal", "city", "plural_noun", "plural_animal", "name", "verb", "adverb", "verb_ending_in_ing", "name", "verb_past", "noun", "place", "verb_ending_in_ing", "adjective", "animal", "verb", "adjective", "plural_noun", "silly_phrase", "color", "verb_ending_in_ing", "number", "name", "verb_ending_in_ing", "plural_animal", "adjective", "adjective"]
                }
            },
            {
                "filename": "weather_report.json",
                "data": {
                    "title": "Unusual Weather Report",
                    "template": "Good evening, I'm [name] with your [adjective] weather forecast. Today, we experienced [adjective] temperatures reaching [number] degrees, causing [plural_noun] to [verb] spontaneously! Tomorrow, a front of [adjective] air will move in from the [direction], bringing a 70% chance of falling [plural_noun]. Residents in [city_name] should prepare by [verb_ending_in_ing] their [plural_noun] and keeping a [noun] handy. The [body_of_water] is expected to turn [color] and begin [verb_ending_in_ing] due to the unusual atmospheric [noun]. Weather experts are [verb_ending_in_ing] in confusion. By [day_of_week], we expect [animal_plural] to rain from the sky, so don't forget your [adjective] umbrella! This has been [name] with your [adjective] weather report. Back to you in the studio!",
                    "placeholders": ["name", "adjective", "adjective", "number", "plural_noun", "verb", "adjective", "direction", "plural_noun", "city_name", "verb_ending_in_ing", "plural_noun", "noun", "body_of_water", "color", "verb_ending_in_ing", "noun", "verb_ending_in_ing", "day_of_week", "animal_plural", "adjective", "name", "adjective"]
                }
            },
            {
                "filename": "video_game.json",
                "data": {
                    "title": "Epic Video Game Adventure",
                    "template": "In the [adjective] video game \"[made_up_title]\", you play as a heroic [occupation] named [character_name] who must save the kingdom of [made_up_place]. Your character can [verb] up to [number] feet and has a special ability to [verb] [plural_noun] with their magical [noun]. The main villain, the evil [title] [villain_name], has stolen all the [plural_noun] and hidden them in a [adjective] castle guarded by [number] [adjective] [creature_plural]. Along your journey, you'll meet a [adjective] sidekick who helps you by [verb_ending_in_ing] [adverb]. The most challenging level is the [place] of [emotion], where you must [verb] across [substance] while avoiding flying [plural_noun]. If you collect enough [color] coins, you can unlock the secret [clothing_item] that makes you [verb] twice as fast! The final boss battle involves [verb_ending_in_ing] the villain until they [verb] and turn into a giant [animal].",
                    "placeholders": ["adjective", "made_up_title", "occupation", "character_name", "made_up_place", "verb", "number", "verb", "plural_noun", "noun", "title", "villain_name", "plural_noun", "adjective", "number", "adjective", "creature_plural", "adjective", "verb_ending_in_ing", "adverb", "place", "emotion", "verb", "substance", "plural_noun", "color", "clothing_item", "verb", "verb_ending_in_ing", "verb", "animal"]
                }
            },
            {
                "filename": "restaurant_review.json",
                "data": {
                    "title": "Restaurant Critic",
                    "template": "I recently visited the new [nationality] restaurant called \"[restaurant_name]\" on [street_name] Street. The atmosphere was [adjective] with [plural_noun] hanging from the ceiling and [adjective] music playing in the background. My server, who introduced themselves as [name], was extremely [adjective] and recommended their signature dish: [food] with [adjective] [food_ingredient] sauce. When the appetizer arrived, it looked like a [noun] that had been [verb_past] for [number] hours. I cautiously took a [adjective] bite and my taste buds began [verb_ending_in_ing] immediately! For the main course, I ordered the [animal] [body_part] served on a bed of [color] [plural_vegetable]. The chef clearly enjoys [verb_ending_in_ing] too much [substance] into everything. The dessert, however, was [adverb] [adjective] – a [adjective] [dessert] topped with [plural_noun]. I give this restaurant [number] out of 5 stars, and would recommend it to anyone who enjoys [verb_ending_in_ing] while they eat.",
                    "placeholders": ["nationality", "restaurant_name", "street_name", "adjective", "plural_noun", "adjective", "name", "adjective", "food", "adjective", "food_ingredient", "noun", "verb_past", "number", "adjective", "verb_ending_in_ing", "animal", "body_part", "color", "plural_vegetable", "verb_ending_in_ing", "substance", "adverb", "adjective", "adjective", "dessert", "plural_noun", "number", "verb_ending_in_ing"]
                }
            },
            {
                "filename": "love_letter.json",
                "data": {
                    "title": "Ridiculous Love Letter",
                    "template": "My [adjective] [term_of_endearment],\n\nEver since I [verb_past] you at the [place], I haven't been able to stop [verb_ending_in_ing] about you. Your [body_part_plural] are like [plural_noun], and your [adjective] smile makes my [body_part] [verb] with joy. You are more [adjective] than a [noun] full of [plural_noun].\n\nWhen you [verb], it sounds like a [animal] [verb_ending_in_ing] in a field of [plural_flower]. I want to [verb] with you under the [celestial_body] and whisper [adjective] nothings into your [body_part].\n\nYesterday, I wrote a [adjective] poem about your [body_part], but my [animal] ate it. I've enclosed a [adjective] [noun] to show my affection. Please [verb] me soon, as I'm [adverb] [verb_ending_in_ing] for your reply.\n\n[adverb] yours,\n[silly_name]",
                    "placeholders": ["adjective", "term_of_endearment", "verb_past", "place", "verb_ending_in_ing", "body_part_plural", "plural_noun", "adjective", "body_part", "verb", "adjective", "noun", "plural_noun", "verb", "animal", "verb_ending_in_ing", "plural_flower", "verb", "celestial_body", "adjective", "body_part", "adjective", "body_part", "animal", "adjective", "noun", "verb", "adverb", "verb_ending_in_ing", "adverb", "silly_name"]
                }
            },
            {
                "filename": "tech_support.json",
                "data": {
                    "title": "Tech Support Nightmare",
                    "template": "Hello, thank you for calling [company_name] tech support. My name is [name], how may I [verb] you today? Your computer is doing WHAT with [plural_noun]? Have you tried [verb_ending_in_ing] it off and on again? OK, let's try something else. First, [verb] your [computer_part] and count to [number] [adverb]. Now, press the [color] button while [verb_ending_in_ing] the [noun]. Do you see a message about [plural_animal] on your screen? That's [adjective]! Next, try [verb_ending_in_ing] into the [adjective] drive. What's that? Your [noun] is now [verb_ending_in_ing] and making a sound like a [animal] [verb_ending_in_ing] underwater? Please [verb] your [software_name] and delete any files that look like [plural_noun]. Still not working? I'll need to transfer you to our [adjective] specialist who deals with [adjective] [plural_noun]. Please hold while I [verb] your call. *[adverb] plays [genre] music*",
                    "placeholders": ["company_name", "name", "verb", "plural_noun", "verb_ending_in_ing", "verb", "computer_part", "number", "adverb", "color", "verb_ending_in_ing", "noun", "plural_animal", "adjective", "verb_ending_in_ing", "adjective", "noun", "verb_ending_in_ing", "animal", "verb_ending_in_ing", "verb", "software_name", "plural_noun", "adjective", "adjective", "plural_noun", "verb", "adverb", "genre"]
                }
            }
        ]
        
        # Save templates to files
        for template in templates:
            filepath = os.path.join(templates_dir, template["filename"])
            if not os.path.exists(filepath):
                with open(filepath, "w") as file:
                    json.dump(template["data"], file, indent=2)

    def use_example_prompt(self, example):
        """Use an example prompt"""
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", example)

    def generate_ai_template(self):
        """Generate a Mad Lib template using OpenAI API"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("API Key Required", "Please enter your OpenAI API key.")
            return
        
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Prompt Required", "Please enter a description for your Mad Lib.")
            return
        
        complexity = self.complexity_var.get()
        style = self.style_var.get()
        
        # Update UI to show we're working
        self.generate_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Generating template... Please wait.")
        self.root.update()
        
        try:
            # Import here to avoid requiring the package if not using this feature
            import requests
            import json
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # Create the system prompt
            system_prompt = f"""You are a creative Mad Libs template generator. 
Create a {complexity.lower()} complexity, {style.lower()}-style Mad Lib template based on the user's description.

Your response should be in JSON format with the following structure:
{{
  "title": "Title of the Mad Lib",
  "template": "The template text with [placeholder] words in brackets",
  "placeholders": ["placeholder1", "placeholder2", ...]
}}

Guidelines:
1. Use [noun], [verb], [adjective], etc. for placeholders
2. Be specific with placeholders like [animal], [color], [food], etc.
3. Include 10-20 placeholders depending on complexity
4. Make sure each placeholder in the template is also in the placeholders list
5. The template should be coherent and fun to play
6. Ensure the story makes sense when placeholders are filled in
7. Use creative and varied placeholders
"""
            
            # Prepare the API request data
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            # Make the API request
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                    headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Try to parse the JSON response
                try:
                    # Find JSON in the response (in case there's additional text)
                    import re
                    json_match = re.search(r'({[\s\S]*})', content)
                    if json_match:
                        content = json_match.group(1)
                    
                    template_data = json.loads(content)
                    
                    # Validate the template data
                    if "title" not in template_data or "template" not in template_data or "placeholders" not in template_data:
                        raise ValueError("Missing required fields in template data")
                    
                    # Store the generated template
                    self.generated_template = template_data
                    
                    # Display the template
                    self.result_text.config(state=tk.NORMAL)
                    self.result_text.delete("1.0", tk.END)
                    self.result_text.insert("1.0", f"Title: {template_data['title']}\n\n")
                    self.result_text.insert(tk.END, f"Template:\n{template_data['template']}\n\n")
                    self.result_text.insert(tk.END, f"Placeholders:\n{', '.join(template_data['placeholders'])}")
                    self.result_text.config(state=tk.DISABLED)
                    
                    # Enable the use template button
                    self.use_template_btn.config(state=tk.NORMAL)
                    
                    self.status_label.config(text="Template generated successfully!")
                except Exception as e:
                    self.status_label.config(text=f"Error parsing response: {str(e)}")
                    messagebox.showerror("Error", f"Failed to parse the generated template: {str(e)}")
            else:
                error_msg = f"API Error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data and "message" in error_data["error"]:
                        error_msg = f"API Error: {error_data['error']['message']}"
                except:
                    pass
                
                self.status_label.config(text=error_msg)
                messagebox.showerror("API Error", error_msg)
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Re-enable the generate button
            self.generate_btn.config(state=tk.NORMAL)

    def use_generated_template(self):
        """Use the generated template in the Create tab"""
        if not hasattr(self, 'generated_template'):
            return
        
        # Load the template into the current madlib
        self.current_madlib = self.generated_template.copy()
        
        # Update UI
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.generated_template["title"])
        
        self.template_text.delete("1.0", tk.END)
        self.template_text.insert("1.0", self.generated_template["template"])
        
        self.placeholders_list.delete(0, tk.END)
        for p in self.generated_template["placeholders"]:
            self.placeholders_list.insert(tk.END, p)
        
        # Switch to create tab
        self.notebook.select(0)
        
        messagebox.showinfo("Success", "Generated template loaded into the Create tab. You can now edit it if needed.")

def main():
    root = tk.Tk()
    app = MadLibsCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 