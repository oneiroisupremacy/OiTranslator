import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import json
import threading
import time
import socket
import sys
from core.glm_engine import GLMEngine
from core.parser import get_parser

class OiTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Oi Translator") 
        self.root.geometry="680x680"

        self.config = self.load_config()
        self.api_key = self.config.get("api_key", "")
        self.process_queue = [] 
        self.is_running = False
        self.is_paused = False 
        
        self.create_widgets()

    def load_config(self):
        if not os.path.exists("config.json"):
            return {"api_key": "", "model": "glm-4.6v-flash", "suffix": "_{lang}"}
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except:
            return {"api_key": "", "model": "glm-4.6v-flash", "suffix": "_{lang}"}

    def save_config(self):
        self.config["api_key"] = self.entry_api.get()
        self.config["model"] = self.model_var.get()
        self.config["suffix"] = self.suffix_var.get()
        with open("config.json", "w") as f:
            json.dump(self.config, f)

    def create_widgets(self):
        frame_api = tk.LabelFrame(self.root, text="API Configuration", padx=10, pady=10)
        frame_api.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_api, text="ZhipuAI API Key:").pack(side="left")
        self.entry_api = tk.Entry(frame_api, width=20, show="*")
        self.entry_api.pack(side="left", padx=5)
        self.entry_api.insert(0, self.api_key)
        
        tk.Label(frame_api, text="Model:").pack(side="left", padx=(10, 5))
        self.model_var = tk.StringVar(value=self.config.get("model", "glm-4.6v-flash"))
        combo_models = ttk.Combobox(frame_api, textvariable=self.model_var, width=15, 
                                    values=["glm-4.6v-flash", "glm-4.5-flash", "glm-4v", "glm-4-flash", "glm-3-turbo"])
        combo_models.pack(side="left")

        btn_save_key = tk.Button(frame_api, text="Save", command=self.save_api_key)
        btn_save_key.pack(side="left", padx=5)

        frame_io = tk.LabelFrame(self.root, text="Input Source", padx=10, pady=10)
        frame_io.pack(fill="x", padx=10, pady=5)

        btn_frame = tk.Frame(frame_io)
        btn_frame.pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="Add Single File", bg="#e1e1e1", command=self.add_single_file).pack(side="left", expand=True, fill="x", padx=2)
        tk.Button(btn_frame, text="Add Batch Folder", bg="#e1e1e1", command=self.add_batch_folder).pack(side="left", expand=True, fill="x", padx=2)
        
        tk.Button(frame_io, text="Clear Selection", command=self.clear_selections).pack(fill="x", pady=2)

        self.lbl_input = tk.Label(frame_io, text="No files or folders selected.", fg="gray", wraplength=650, justify="left")
        self.lbl_input.pack(anchor="w", pady=5)

        frame_set = tk.LabelFrame(self.root, text="Translation Settings", padx=10, pady=10)
        frame_set.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_set, text="Target Language:").grid(row=0, column=0, sticky="w")
        self.lang_var = tk.StringVar(value="Indonesian")
        tk.Entry(frame_set, textvariable=self.lang_var, width=20).grid(row=0, column=1)

        tk.Label(frame_set, text="Output Suffix:").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.suffix_var = tk.StringVar(value=self.config.get("suffix", "_{lang}"))
        entry_suffix = tk.Entry(frame_set, textvariable=self.suffix_var, width=15)
        entry_suffix.grid(row=0, column=3)
        tk.Label(frame_set, text="(Use {lang})", font=("Arial", 8), fg="gray").grid(row=0, column=4, sticky="w")

        tk.Label(frame_set, text="Speed Mode:").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.speed_var = tk.StringVar(value="Standard")
        combo_speed = ttk.Combobox(frame_set, textvariable=self.speed_var, values=["Safe", "Standard", "Aggressive"], state="readonly")
        combo_speed.grid(row=1, column=1, pady=(10,0))

        btn_frame_action = tk.Frame(self.root)
        btn_frame_action.pack(pady=10)
        
        self.btn_start = tk.Button(btn_frame_action, text="START TRANSLATION", bg="#007acc", fg="white", font=("Arial", 12, "bold"), command=self.start_translation_thread)
        self.btn_start.pack(side="left", padx=5)
        
        self.btn_pause = tk.Button(btn_frame_action, text="PAUSE", bg="#ffaa00", fg="white", font=("Arial", 12, "bold"), state="disabled", command=self.toggle_pause)
        self.btn_pause.pack(side="left", padx=5)
        
        self.btn_stop = tk.Button(btn_frame_action, text="STOP", bg="#ff4444", fg="white", font=("Arial", 12, "bold"), state="disabled", command=self.stop_process)
        self.btn_stop.pack(side="left", padx=5)

        self.lbl_status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=5, font=("Consolas", 10))
        self.lbl_status.pack(fill="x", padx=10, pady=(0, 5))

        frame_log = tk.Frame(self.root)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(frame_log, height=10)
        self.log_text.pack(side="left", fill="both", expand=True)
        self.log_text.tag_config("pause_text", foreground="orange", font=("Arial", 10, "bold"))

        btn_frame_util = tk.Frame(self.root)
        btn_frame_util.pack(fill="x", padx=10, pady=(0, 5), anchor="e")
        tk.Button(btn_frame_util, text="Copy Log", command=self.copy_log).pack(side="right")

    def check_internet(self):
        try:
            socket.setdefaulttimeout(1)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except OSError:
            return False

    def copy_log(self):
        content = self.log_text.get("1.0", "end-1c")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Log content copied to clipboard!")

    def save_api_key(self):
        key = self.entry_api.get()
        model = self.model_var.get()
        suffix = self.suffix_var.get()
        self.config["api_key"] = key
        self.config["model"] = model
        self.config["suffix"] = suffix
        with open("config.json", "w") as f:
            json.dump(self.config, f)
        messagebox.showinfo("Success", "Settings saved!")

    def add_single_file(self):
        file_path = filedialog.askopenfilename(title="Select Subtitle File", filetypes=[("Subtitle Files", "*.srt *.vtt"), ("All Files", "*.*")])
        if file_path:
            self.process_queue.append(file_path)
            self.update_input_label()

    def add_batch_folder(self):
        folder_path = filedialog.askdirectory(title="SelectFolder")
        if folder_path:
            self.process_queue.append(folder_path)
            self.update_input_label()

    def clear_selections(self):
        self.process_queue = []
        self.update_input_label()

    def update_input_label(self):
        count = len(self.process_queue)
        if count == 0:
            self.lbl_input.config(text="No files or folders selected.")
        else:
            self.lbl_input.config(text=f"{count} target(s) added to queue.")

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update()

    def toggle_pause(self):
        if self.is_paused:
            if self.check_internet():
                self.is_paused = False
                self.btn_pause.config(text="PAUSE", bg="#ffaa00")
                self.log("Process Resumed.")
            else:
                messagebox.showwarning("No Internet", "Internet still disconnected. Cannot resume.")
        else:
            self.is_paused = True
            self.btn_pause.config(text="RESUME", bg="#00cc00")
            self.log("Process Paused.")

    def stop_process(self):
        self.is_running = False
        self.is_paused = False
        self.log("Process stopped by user.")
        self.btn_stop.config(state="disabled")
        self.btn_pause.config(state="disabled")
        self.btn_start.config(state="normal") 
        self.lbl_status.config(text="Ready")

    def format_eta(self, seconds):
        if seconds < 0 or seconds > 1000000:
            return "--:--:--"
        h, remainder = divmod(int(seconds), 3600)
        m, s = divmod(remainder, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def pre_scan_files(self, files_list):
        total_lines = 0
        files_data = []
        self.log("Scanning files for progress estimation...")
        
        for file_path in files_list:
            if not self.is_running: break
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in ['.srt', '.vtt']: continue
            
            parser, _ = get_parser(ext)
            if parser:
                try:
                    subs = parser(file_path)
                    line_count = len(subs)
                    total_lines += line_count
                    files_data.append({'path': file_path, 'count': line_count, 'ext': ext, 'filename': os.path.basename(file_path)})
                except: continue
        return total_lines, files_data

    def start_translation_thread(self):
        raw_key = self.entry_api.get()
        if not raw_key:
            messagebox.showwarning("Error", "API Key is empty!")
            return
        if len(raw_key) < 10:
            messagebox.showwarning("Error", "API Key looks too short.")
            return
            
        self.is_running = True
        self.is_paused = False
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.btn_pause.config(state="normal", text="PAUSE", bg="#ffaa00")
        threading.Thread(target=self.run_translation, daemon=True).start()

    def run_translation(self):
        self.log("Initializing translation engine...")
        
        api_key = self.entry_api.get().strip()
        model_name = self.model_var.get() 
        
        if len(api_key) > 5:
            masked_key = api_key[:4] + "****" + api_key[-4:]
        else:
            masked_key = "SHORT_KEY"
            
        self.log(f"API Key loaded: {masked_key}")
        self.log(f"Primary Model: {model_name}")
        
        engine = GLMEngine(api_key, model=model_name)
        target_lang = self.lang_var.get()
        mode = self.speed_var.get()
        
        raw_files_list = []
        for item in self.process_queue:
            if os.path.isfile(item):
                if item.lower().endswith(('.srt', '.vtt')):
                    raw_files_list.append(item)
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        if file.lower().endswith(('.srt', '.vtt')):
                            raw_files_list.append(os.path.join(root, file))

        total_lines_all, processed_files_data = self.pre_scan_files(raw_files_list)
        total_files = len(processed_files_data)
        
        self.log(f"Found {total_files} valid files with {total_lines_all} total subtitle lines.")
        
        if total_files == 0:
            self.log("No valid subtitle files found.")
            self.is_running = False
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")
            self.btn_pause.config(state="disabled")
            self.lbl_status.config(text="Ready")
            return

        start_time = time.time()
        lines_processed = 0
        success_count = 0
        
        for i, file_data in enumerate(processed_files_data):
            if not self.is_running:
                break
            
            while self.is_paused:
                if not self.is_running: break
                if self.check_internet():
                    self.btn_pause.config(text="RESUME (Net OK)", bg="#00cc00")
                else:
                    self.btn_pause.config(text="RESUME (No Net)", bg="#ff4444")
                time.sleep(0.5)
            
            if not self.is_running: break

            try:
                file_path = file_data['path']
                filename = file_data['filename']
                ext = file_data['ext']

                file_start_time = time.time()
                
                self.log(f"[{i+1}/{total_files}] Processing: {filename}")
                
                parser, writer = get_parser(ext)
                subs = parser(file_path)
                
                for idx, sub in enumerate(subs):
                    if not self.is_running: 
                        break
                    
                    while self.is_paused:
                        if not self.is_running: break
                        if self.check_internet():
                            self.btn_pause.config(text="RESUME (Net OK)", bg="#00cc00")
                        else:
                            self.btn_pause.config(text="RESUME (No Net)", bg="#ff4444")
                        time.sleep(0.5)
                    
                    if not self.is_running: break

                    try:
                        translated_text = engine.translate(sub['text'], target_lang, mode)
                        sub['text'] = translated_text
                    except Exception as e:
                        error_msg = str(e)
                        if any(err in error_msg for err in ["ConnectionError", "Timeout", "connect", "Network"]):
                            self.log(f"\n!!! NETWORK ERROR DETECTED !!! Auto-Paused.", "pause_text")
                            self.is_paused = True
                            while self.is_paused:
                                if not self.is_running: break
                                if self.check_internet():
                                    self.btn_pause.config(text="RESUME (Net OK)", bg="#00cc00")
                                else:
                                    self.btn_pause.config(text="RESUME (No Net)", bg="#ff4444")
                                time.sleep(0.5)
                            if self.is_running:
                                translated_text = engine.translate(sub['text'], target_lang, mode)
                                sub['text'] = translated_text
                        else:
                            translated_text = sub['text']
                    
                    lines_processed += 1
                    percent = int((lines_processed / total_lines_all) * 100)
                    
                    current_time = time.time()
                    elapsed = current_time - start_time
                    
                    if lines_processed > 0:
                        avg_time_per_line = elapsed / lines_processed
                        remaining_lines = total_lines_all - lines_processed
                        eta_seconds = avg_time_per_line * remaining_lines
                        eta_str = self.format_eta(eta_seconds)
                    else:
                        eta_str = "Calculating..."
                        
                    status_msg = f"Total Progress: {percent}% | ETA: {eta_str} | File: {filename}"
                    self.lbl_status.config(text=status_msg)

                    display_text = translated_text
                    if len(display_text) >= 10:
                        display_text = f"{display_text[:5]}...{display_text[-5:]}"  
                    print(f"Translation OK using model: {engine.current_active_model} [{display_text}] [{sub['time']}]")
                if not self.is_running: break

                output_dir = os.path.join(os.getcwd(), "output")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                suffix_raw = self.suffix_var.get()
                suffix_final = suffix_raw.replace("{lang}", target_lang)
                base_filename = os.path.splitext(filename)[0]
                output_filename = f"{base_filename}{suffix_final}{ext}"
                output_full_path = os.path.join(output_dir, output_filename)
                
                writer(output_full_path, subs)

                file_elapsed = time.time() - file_start_time
                time_str = self.format_eta(file_elapsed)
                
                self.log(f"  Finished: {output_filename} | Time: {time_str}")
                success_count += 1
                
                print("Translation Completed, Next")

            except Exception as e:
                self.log(f"  ERROR: {str(e)}")

        self.log("========================================")
        self.log(f"TASK COMPLETED. Processed {success_count}/{total_files} files.")
        self.is_running = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.btn_pause.config(state="disabled", text="PAUSE", bg="#ffaa00")
        self.lbl_status.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = OiTranslatorApp(root)
    root.mainloop()
