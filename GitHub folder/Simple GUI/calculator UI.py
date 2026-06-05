import tkinter as tk

root = tk.Tk()
root.title("Calculator")       
root.resizable(False, False)   
root.configure(bg="#1e1e1e")   

COLOR_BG        = "#1e1e1e"   
COLOR_DISPLAY   = "#2b2b2b"   
COLOR_BTN_NUM   = "#3a3a3a"   
COLOR_BTN_OP    = "#505050"   
COLOR_BTN_EQ    = "#f5a623"   
COLOR_BTN_AC    = "#e05c5c"   
COLOR_TEXT      = "#ffffff"   
COLOR_TEXT_DIM  = "#888888"   

FONT_DISPLAY    = ("Courier New", 28, "bold")   
FONT_EXPR       = ("Courier New", 13)           
FONT_BTN        = ("Courier New", 18, "bold")   

expression = ""          
result_var = tk.StringVar(value="0")    
expr_var   = tk.StringVar(value="")    

def press_num(n):
    """Called when a number button (0-9) or dot is clicked."""
    global expression
    current = result_var.get()
    if current == "0" or current == "Error":
        result_var.set(n)
    else:
        result_var.set(current + n)


def press_op(op):
    """Called when +  -  *  /  is clicked."""
    global expression
    expression = result_var.get() + " " + op + " "
    expr_var.set(expression)     
    result_var.set("0")          

def press_equals():
    """Called when = is clicked. Evaluates the expression."""
    global expression

    if expression == "":
        return 

    full_expr = expression + result_var.get()   
    expr_var.set(full_expr + " =")              

    try:
        answer = round(eval(full_expr), 10)

        if answer == int(answer):
            answer = int(answer)

        result_var.set(str(answer))
    except ZeroDivisionError:
        result_var.set("Error")     
    except Exception:
        result_var.set("Error")     
    expression = ""   


def press_clear():
    """Called when AC is clicked. Resets everything."""
    global expression
    expression = ""
    result_var.set("0")
    expr_var.set("")


def press_delete():
    """Called when ⌫ is clicked. Removes last character."""
    current = result_var.get()
    if current == "Error":
        result_var.set("0")
    elif len(current) > 1:
        result_var.set(current[:-1])   
    else:
        result_var.set("0")            

display_frame = tk.Frame(root, bg=COLOR_DISPLAY, padx=16, pady=12)
display_frame.pack(fill=tk.X, padx=12, pady=(12, 6))

expr_label = tk.Label(
    display_frame,           
    textvariable=expr_var,   
    font=FONT_EXPR,
    fg=COLOR_TEXT_DIM,
    bg=COLOR_DISPLAY,
    anchor="e",              
)
expr_label.pack(fill=tk.X)


result_label = tk.Label(
    display_frame,
    textvariable=result_var,  
    font=FONT_DISPLAY,
    fg=COLOR_TEXT,
    bg=COLOR_DISPLAY,
    anchor="e",               
)
result_label.pack(fill=tk.X)



btn_frame = tk.Frame(root, bg=COLOR_BG)
btn_frame.pack(padx=12, pady=(0, 12))


def make_button(parent, text, color, command, row, col, colspan=1):
    """
    Helper function — creates one button and places it in the grid.
    
    Parameters:
      parent  — the Frame this button lives in
      text    — label shown on the button
      color   — background color
      command — function to call when clicked
      row     — grid row position (0 = top)
      col     — grid column position (0 = left)
      colspan — how many columns wide (default 1)
    """
    btn = tk.Button(
        parent,
        text=text,
        font=FONT_BTN,
        fg=COLOR_TEXT,
        bg=color,
        activebackground=color,      
        activeforeground=COLOR_TEXT,
        relief=tk.FLAT,             
        cursor="hand2",              
        width=4,
        command=command,             
    )

    btn.grid(
        row=row, column=col,
        columnspan=colspan,
        padx=4, pady=4,
        sticky="nsew"
    )

    # Hover effect — lighten the button when mouse enters
    btn.bind("<Enter>", lambda e: btn.config(bg=lighten(color)))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))

    return btn


def lighten(hex_color):
    """Returns a slightly lighter version of a hex color for hover effect."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = min(255, r + 30)
    g = min(255, g + 30)
    b = min(255, b + 30)
    return f"#{r:02x}{g:02x}{b:02x}"


make_button(btn_frame, "AC", COLOR_BTN_AC,  press_clear,         row=0, col=0)
make_button(btn_frame, "⌫", COLOR_BTN_OP,  press_delete,        row=0, col=1)
make_button(btn_frame, "/", COLOR_BTN_OP,  lambda: press_op("/"), row=0, col=2)
make_button(btn_frame, "*", COLOR_BTN_OP,  lambda: press_op("*"), row=0, col=3)

# Row 1 — 7 8 9 -
make_button(btn_frame, "7", COLOR_BTN_NUM, lambda: press_num("7"), row=1, col=0)
make_button(btn_frame, "8", COLOR_BTN_NUM, lambda: press_num("8"), row=1, col=1)
make_button(btn_frame, "9", COLOR_BTN_NUM, lambda: press_num("9"), row=1, col=2)
make_button(btn_frame, "-", COLOR_BTN_OP,  lambda: press_op("-"),  row=1, col=3)

# Row 2 — 4 5 6 +
make_button(btn_frame, "4", COLOR_BTN_NUM, lambda: press_num("4"), row=2, col=0)
make_button(btn_frame, "5", COLOR_BTN_NUM, lambda: press_num("5"), row=2, col=1)
make_button(btn_frame, "6", COLOR_BTN_NUM, lambda: press_num("6"), row=2, col=2)
make_button(btn_frame, "+", COLOR_BTN_OP,  lambda: press_op("+"),  row=2, col=3)

# Row 3 — 1 2 3 (empty)
make_button(btn_frame, "1", COLOR_BTN_NUM, lambda: press_num("1"), row=3, col=0)
make_button(btn_frame, "2", COLOR_BTN_NUM, lambda: press_num("2"), row=3, col=1)
make_button(btn_frame, "3", COLOR_BTN_NUM, lambda: press_num("3"), row=3, col=2)

# Row 4 — 0 (wide), dot, equals
make_button(btn_frame, "0", COLOR_BTN_NUM, lambda: press_num("0"), row=4, col=0, colspan=2)
make_button(btn_frame, ".", COLOR_BTN_NUM, lambda: press_num("."), row=4, col=2)
make_button(btn_frame, "=", COLOR_BTN_EQ,  press_equals,           row=3, col=3, colspan=1)

# Row 3+4 — equals button spans 2 rows
# We re-place it using grid directly for rowspan
btn_frame.grid_slaves(row=3, column=3)[0].grid(
    row=3, column=3, rowspan=2, padx=4, pady=4, sticky="nsew"
)


def on_key(event):
    key = event.char
    if key in "0123456789":
        press_num(key)
    elif key == ".":
        press_num(".")
    elif key in "+-*/":
        press_op(key)
    elif key in ("\r", "="):   
        press_equals()
    elif event.keysym == "BackSpace":
        press_delete()
    elif event.keysym == "Escape":
        press_clear()

root.bind("<Key>", on_key)   
root.mainloop()