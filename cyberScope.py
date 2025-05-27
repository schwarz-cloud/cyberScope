import tkinter as tk
from tkinter import messagebox, scrolledtext
from threading import Thread
import subprocess
import socket
import sys
import re 

sublist3r_path = 'C:\\Users\\nzd\\AppData\\Roaming\\Python\\Python312\\site-packages\\sublist3r.py'
dalfox_path = "C:\\Users\\nzd\\go\\bin\\dalfox.exe"
sqlmap_path = "C:\\Users\\nzd\\OneDrive\\Desktop\\ecc201 project\\sqlmap-master\\sqlmap.py"
nmap_path = 'C:\\Users\\nzd\\Nmap\\nmap.exe'



root = tk.Tk()
root.title("CyberScope")
root.geometry("500x500")  # Increase the size to better fit the buttons
root.configure(bg='black')
root.resizable(width=False, height=False)


subdomains_list = []

def show_results_in_new_window(subdomains):
    results_window = tk.Toplevel(root)
    results_window.title("Subdomain Results")
    results_text_area = scrolledtext.ScrolledText(results_window, height=20, width=80)
    results_text_area.pack()
    
    for subdomain in subdomains: 
        results_text_area.insert(tk.END, subdomain + "\n")
    results_text_area.config(state=tk.DISABLED) 
    

def find_subdomains(domain):
    process = subprocess.Popen(['python', sublist3r_path, '-d', domain, '-o', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        print("Error:", stderr.decode())
    subdomains = stdout.decode().splitlines()

    global subdomains_list
    subdomains_list = [line.strip() for line in subdomains if line.strip() and not line.startswith("[") and not line.startswith("[-]") and "Error:" not in line and "# Coded By" not in line and "-" not in line]
  
    show_results_in_new_window(subdomains_list)
       

def run_dalfox(url):
    results_window = tk.Toplevel(root)
    results_window.title("XSS Check Results")
    results_text_area = scrolledtext.ScrolledText(results_window, height=20, width=80)
    results_text_area.pack()

    command = [dalfox_path, 'url', url]
    print(f"Running Dalfox with command: {' '.join(command)}")  # Debugging print statement

    # Specify utf-8 encoding and handle errors by replacing non-decodable characters
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')

    def read_output(pipe, text_widget):
        while True:
            line = pipe.readline()
            if not line:
                break
            text_widget.insert(tk.END, line)
            text_widget.see(tk.END)
            text_widget.update_idletasks()
        pipe.close()

    # Start threads to read stdout and stderr, update the text widget in the GUI
    Thread(target=read_output, args=(process.stdout, results_text_area)).start()
    Thread(target=read_output, args=(process.stderr, results_text_area)).start()

    # Wait for the process to complete and update the GUI accordingly
    def wait_for_process(proc, text_widget):
        proc.wait()
        text_widget.insert(tk.END, "\nXSS check complete.")
        text_widget.config(state=tk.DISABLED)

    Thread(target=wait_for_process, args=(process, results_text_area)).start()

def run_sqlmap(target_url):
    python_executable = sys.executable
    command = [python_executable, sqlmap_path, '-u', target_url, '--batch']
    results_window = tk.Toplevel(root)
    results_window.title("SQL Injection Check Results")
    results_text_area = scrolledtext.ScrolledText(results_window, height=20, width=80)
    results_text_area.pack()

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')

    def read_output(pipe, text_widget):
        while True:
            line = pipe.readline()
            if not line:
                break
            text_widget.insert(tk.END, line)
            text_widget.see(tk.END)
            text_widget.update_idletasks()
        pipe.close()

    # Start threads to read stdout and stderr, update the text widget in the GUI
    Thread(target=read_output, args=(process.stdout, results_text_area)).start()
    Thread(target=read_output, args=(process.stderr, results_text_area)).start()

    # Wait for the process to complete and update the GUI accordingly
    def wait_for_process(proc, text_widget):
        proc.wait()
        text_widget.insert(tk.END, "\nSQL Injection check complete.")
        text_widget.config(state=tk.DISABLED)

    Thread(target=wait_for_process, args=(process, results_text_area)).start()
      
def run_nmap(target_host):
    results_window = tk.Toplevel(root)
    results_window.title("Nmap Scan Results")
    results_text_area = scrolledtext.ScrolledText(results_window, height=20, width=80)
    results_text_area.pack()

    command = [nmap_path, '-p', '1-1000', target_host]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')

    def read_output(pipe, text_widget):
        while True:
            line = pipe.readline()
            if not line:
                break
            text_widget.insert(tk.END, line)
            text_widget.see(tk.END)
            text_widget.update_idletasks()
        pipe.close()

    Thread(target=read_output, args=(process.stdout, results_text_area)).start()
    Thread(target=read_output, args=(process.stderr, results_text_area)).start()

    def wait_for_process(proc, text_widget):
        proc.wait()
        text_widget.insert(tk.END, "\nNmap scan complete.")
        text_widget.config(state=tk.DISABLED)

    Thread(target=wait_for_process, args=(process, results_text_area)).start()




#input validation 

# Regular expression patterns for validation

try : 
       domain_pattern = re.compile(r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]+/?([a-zA-Z0-9._-]+/?)*$')
       url_pattern = re.compile(r'^https?://(www\.)?[a-z0-9.-]+(\.[a-z]{2,})+([\/\w \.-]*)*\/?\??([\w=&]+/?)*$')
       ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
finally: 
       def is_valid_domain_or_url(input_str):
           return domain_pattern.match(input_str) or url_pattern.match(input_str)
       def on_find_button_click():
           domain = entry.get()
           if is_valid_domain_or_url(domain):
                  Thread(target=find_subdomains, args=(domain,)).start()
           else:
                  messagebox.showerror("Error", "Please enter a valid domain")

       def on_xss_button_click():
             url = entry.get()
             if url_pattern.match(url):
                 Thread(target=run_dalfox, args=(url,)).start()
             else:
                messagebox.showerror("Error", "Please enter a valid URL starting with http:// or https://")

       def on_sqli_button_click():
             url = entry.get()
             if is_valid_domain_or_url(url):
                 Thread(target=run_sqlmap, args=(url,)).start()
             else:
                 messagebox.showerror("Error", "Please enter a valid URL starting with http:// or https://")

       def on_nmap_button_click():
             target = entry.get()
             if is_valid_domain_or_url(target) or ip_pattern.match(target):
                 Thread(target=run_nmap, args=(target,)).start()
                 
             else:
                 messagebox.showerror("Error", "Please enter a valid IP address or host")






def create_neon_button(canvas, text, command, x, y, width, height):
    def on_click(event):
        command()

    # Draw the button with neon effect
    button_bg = canvas.create_rectangle(x, y, x + width, y + height, outline="#00FFFF", fill="black", width=2)
    button_text = canvas.create_text(x + width / 2, y + height / 2, text=text, fill="#00FFFF", font=('Arial', 10, 'bold'))

    # Bind the button to the provided command
    canvas.tag_bind(button_bg, '<Button-1>', on_click)
    canvas.tag_bind(button_text, '<Button-1>', on_click)

    # Add hover effects
    canvas.tag_bind(button_bg, '<Enter>', lambda e: canvas.itemconfig(button_bg, fill='#005555'))
    canvas.tag_bind(button_bg, '<Leave>', lambda e: canvas.itemconfig(button_bg, fill='black'))
    canvas.tag_bind(button_text, '<Enter>', lambda e: canvas.itemconfig(button_bg, fill='#005555'))
    canvas.tag_bind(button_text, '<Leave>', lambda e: canvas.itemconfig(button_bg, fill='black'))
    return button_bg, button_text

# Function to create a neon-style tooltip on a canvas
def show_tooltip(canvas, tooltip_text):
    canvas.itemconfig(tooltip_text, state='normal')

# Function to hide the tooltip text
def hide_tooltip(canvas, tooltip_text):
    canvas.itemconfig(tooltip_text, state='hidden')

# Function to create a neon-style tooltip text without a background rectangle
def  create_neon_tooltip(canvas, text, x, y):
    # Draw the tooltip text and initially hide it
    tooltip_text= canvas.create_text(x, y, text=text, fill="#00FFFF", font=('Arial', 8, 'bold'), state='hidden')
    return tooltip_text


# Entry label and entry widget
entry_label = tk.Label(root, text="Enter domain or URL:", bg='black', fg='#00FFFF')
entry_label.pack(pady=(100,0))  # Add padding to separate from the top edge
entry = tk.Entry(root, width=50)
entry.pack(pady=(5,20))  # Add padding for spacing

# Create a canvas to hold the neon-style buttons
button_canvas = tk.Canvas(root, bg='black', highlightthickness=0)
button_canvas.pack(fill=tk.BOTH, expand=True)

# Positioning variables for the buttons
canvas_width = 500
button_width = 300
button_height = 40
x_position = (canvas_width - button_width) / 2

# Create neon-style buttons centered on the canvas
create_neon_button(button_canvas, "Find Subdomains", on_find_button_click, x_position, 10, button_width, button_height)

#button_canvas.itemconfig(tooltip_bg, state='hidden')

dalfox_button_bg, dalfox_button_text = create_neon_button(button_canvas, "XSS Check", on_xss_button_click, x_position, 60, button_width, button_height)
create_neon_button(button_canvas, "Check SQL Injection", on_sqli_button_click, x_position, 110, button_width, button_height)
create_neon_button(button_canvas, "Run Nmap Scan", on_nmap_button_click, x_position, 160, button_width, button_height)

# Bind the tooltip to the "XSS Check with Dalfox" button
tooltip_text = create_neon_tooltip(button_canvas, 
                                               "Insert a full URL: https://www.example.com or http://www.example.com", 
                                                 230, 230)
button_canvas.itemconfig(tooltip_text, state='hidden')
button_canvas.tag_bind(dalfox_button_bg, '<Enter>', lambda event: show_tooltip(button_canvas, tooltip_text))
button_canvas.tag_bind(dalfox_button_bg, '<Leave>', lambda event: hide_tooltip(button_canvas, tooltip_text))
button_canvas.tag_bind(dalfox_button_text, '<Enter>', lambda event: show_tooltip(button_canvas, tooltip_text))
button_canvas.tag_bind(dalfox_button_text, '<Leave>', lambda event: hide_tooltip(button_canvas, tooltip_text))


root.mainloop()