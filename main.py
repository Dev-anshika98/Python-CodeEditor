from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# Colors and Fonts
BG_COLOR = "#2b2b2b"
TEXT_COLOR = "#dcdcdc"
FONT = ("Consolas", 12)
BUTTON_FONT = ("Arial", 12, "bold")
BUTTON_COLOR = "#4CAF50"
BUTTON_TEXT_COLOR = "#ffffff"
CURSOR_COLOR = "#000000" 

compiler = Tk()
compiler.title('My Fantastic IDE')
compiler.geometry("800x600")
compiler.configure(bg=BG_COLOR)
file_path = ''

def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def run():
    if file_path == '':
        save_prompt = Toplevel()
        save_prompt.title('Save your code')
        save_prompt.geometry("300x100")
        save_prompt.configure(bg=BG_COLOR)
        text = Label(save_prompt, text='Please save your code', font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
        text.pack(expand=True)
        return

    def get_user_input():
        user_input = input_text.get('1.0', END)
        save_prompt.destroy()
        execute_code(user_input)

    def execute_code(user_input):
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate(input=user_input.encode())
        code_output.delete('1.0', END)
        code_output.insert('1.0', output.decode())
        code_output.insert('1.0', error.decode())

    save_prompt = Toplevel()
    save_prompt.title('User Input Required')
    save_prompt.geometry("400x200")
    save_prompt.configure(bg=BG_COLOR)
    text = Label(save_prompt, text='Provide input for the script:', font=("Arial", 12), bg=BG_COLOR, fg=TEXT_COLOR)
    text.pack(pady=10)
    input_text = Text(save_prompt, height=5, width=40, font=FONT, bg=TEXT_COLOR, fg=BG_COLOR)
    input_text.pack(pady=5)
    submit_button = Button(save_prompt, text='Submit', command=get_user_input, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT)
    submit_button.pack(pady=10)

menu_bar = Menu(compiler, bg=BG_COLOR, fg=TEXT_COLOR)

file_menu = Menu(menu_bar, tearoff=0, bg=BG_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0, bg=BG_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

editor_frame = Frame(compiler, bg=BG_COLOR)
editor_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

editor_label = Label(editor_frame, text="Editor", font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
editor_label.pack(side=TOP, anchor=W)

editor = Text(editor_frame, wrap=NONE, undo=True, font=FONT, bg=TEXT_COLOR, fg=BG_COLOR, insertbackground=CURSOR_COLOR)
editor.pack(fill=BOTH, expand=True, pady=5, padx=5)

scroll_y = Scrollbar(editor_frame, orient=VERTICAL, command=editor.yview, bg=BG_COLOR)
scroll_y.pack(side=RIGHT, fill=Y)
editor.config(yscrollcommand=scroll_y.set)

scroll_x = Scrollbar(editor_frame, orient=HORIZONTAL, command=editor.xview, bg=BG_COLOR)
scroll_x.pack(side=BOTTOM, fill=X)
editor.config(xscrollcommand=scroll_x.set)

output_frame = Frame(compiler, bg=BG_COLOR)
output_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

output_label = Label(output_frame, text="Output", font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR)
output_label.pack(side=TOP, anchor=W)

code_output = Text(output_frame, height=10, wrap=NONE, font=FONT, bg=TEXT_COLOR, fg=BG_COLOR, insertbackground=CURSOR_COLOR)
code_output.pack(fill=BOTH, expand=True, pady=5, padx=5)

scroll_y_output = Scrollbar(output_frame, orient=VERTICAL, command=code_output.yview, bg=BG_COLOR)
scroll_y_output.pack(side=RIGHT, fill=Y)
code_output.config(yscrollcommand=scroll_y_output.set)

scroll_x_output = Scrollbar(output_frame, orient=HORIZONTAL, command=code_output.xview, bg=BG_COLOR)
scroll_x_output.pack(side=BOTTOM, fill=X)
code_output.config(xscrollcommand=scroll_x_output.set)

compiler.mainloop()
