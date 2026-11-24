import os
import sys
import json
import threading
import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DEFAULT_SERVER_URL = "https://maintained-vocals-idol-collective.trycloudflare.com"

class EcuClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🦂 SCORPION REMAP PRO v3.2.0")
        self.geometry("820x650")
        self.minsize(750, 600)

        self.server_url = DEFAULT_SERVER_URL
        self.token = None
        self.user_data = None
        self.selected_file_path = None
        self.solution_vars = {}

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ================= شاشة تسجيل الدخول =================
    def show_login_screen(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self, corner_radius=18, fg_color="#111a2e")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(frame, text="🦂 SCORPION REMAP PRO", font=ctk.CTkFont(size=26, weight="bold"), text_color="#38bdf8")
        title.pack(padx=40, pady=(30, 8))

        subtitle = ctk.CTkLabel(frame, text="برنامج العميل لتعديل كمبيوترات السيارات سحابياً", font=ctk.CTkFont(size=13), text_color="#94a3b8")
        subtitle.pack(padx=40, pady=(0, 25))

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="اسم المستخدم (Username)", width=300, height=42, font=ctk.CTkFont(size=14))
        self.username_entry.pack(padx=40, pady=10)
        self.username_entry.insert(0, "client_demo")

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="كلمة المرور (Password)", show="*", width=300, height=42, font=ctk.CTkFont(size=14))
        self.password_entry.pack(padx=40, pady=10)
        self.password_entry.insert(0, "Client123456")

        self.login_btn = ctk.CTkButton(frame, text="تسجيل الدخول", command=self.handle_login, width=300, height=45, font=ctk.CTkFont(size=15, weight="bold"))
        self.login_btn.pack(padx=40, pady=(20, 15))

        self.status_lbl = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=12), text_color="#f87171")
        self.status_lbl.pack(padx=40, pady=(0, 20))

    def handle_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get().strip()
        if not u or not p:
            self.status_lbl.configure(text="يرجى إدخال اسم المستخدم وكلمة المرور")
            return

        self.login_btn.configure(state="disabled", text="جاري الاتصال بالسيرفر...")
        self.status_lbl.configure(text="")

        def req():
            try:
                resp = requests.post(f"{self.server_url}/api/v1/auth/login", json={"username": u, "password": p}, timeout=15)
                data = resp.json()
                if resp.status_code == 200 and data.get("success"):
                    self.token = data["access_token"]
                    self.user_data = data["user"]
                    self.after(0, self.show_main_screen)
                else:
                    err = data.get("detail", "بيانات الدخول غير صحيحة")
                    self.after(0, lambda: self.login_failed(err))
            except Exception as e:
                self.after(0, lambda: self.login_failed("فشل الاتصال بالسيرفر السحابي"))

        threading.Thread(target=req, daemon=True).start()

    def login_failed(self, msg):
        self.login_btn.configure(state="normal", text="تسجيل الدخول")
        self.status_lbl.configure(text=msg)

    # ================= الشاشة الرئيسية =================
    def show_main_screen(self):
        self.clear_screen()

        # الشريط العلوي
        header = ctk.CTkFrame(self, height=60, corner_radius=12, fg_color="#111a2e")
        header.pack(fill="x", padx=20, pady=(15, 10))

        title = ctk.CTkLabel(header, text="🦂 SCORPION REMAP PRO", font=ctk.CTkFont(size=18, weight="bold"), text_color="#38bdf8")
        title.pack(side="left", padx=20, pady=12)

        logout_btn = ctk.CTkButton(header, text="خروج", width=70, height=32, fg_color="#ef4444", hover_color="#dc2626", command=self.show_login_screen)
        logout_btn.pack(side="right", padx=15, pady=12)

        self.credits_lbl = ctk.CTkLabel(header, text=f"الرصيد: {self.user_data.get('credits', 0)} نقطة ⚡", font=ctk.CTkFont(size=14, weight="bold"), text_color="#4ade80")
        self.credits_lbl.pack(side="right", padx=15, pady=12)

        user_lbl = ctk.CTkLabel(header, text=f"المستخدم: {self.user_data.get('username')}", font=ctk.CTkFont(size=13), text_color="#cbd5e1")
        user_lbl.pack(side="right", padx=10, pady=12)

        # حاوية المحتوى
        content = ctk.CTkScrollableFrame(self, corner_radius=12, fg_color="#0b1120")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # منطقة اختيار الملف
        file_frame = ctk.CTkFrame(content, corner_radius=12, fg_color="#111a2e")
        file_frame.pack(fill="x", pady=10, padx=10)

        self.file_lbl = ctk.CTkLabel(file_frame, text="لم يتم اختيار أي ملف ECU بعد (.bin / .ori)", font=ctk.CTkFont(size=14), text_color="#94a3b8")
        self.file_lbl.pack(side="left", padx=20, pady=20)

        select_btn = ctk.CTkButton(file_frame, text="📁 اختيار ملف السيارة", command=self.select_file, height=40, font=ctk.CTkFont(size=14, weight="bold"))
        select_btn.pack(side="right", padx=20, pady=20)

        # بطاقة معلومات السيارة
        self.info_frame = ctk.CTkFrame(content, corner_radius=12, fg_color="#111a2e")
        self.info_frame.pack(fill="x", pady=10, padx=10)

        info_title = ctk.CTkLabel(self.info_frame, text="بيانات الملف والكمبيوتر (ECU Information):", font=ctk.CTkFont(size=15, weight="bold"), text_color="#38bdf8")
        info_title.pack(anchor="w", padx=20, pady=(15, 10))

        self.info_text = ctk.CTkLabel(self.info_frame, text="الشركة: -- | الموديل: -- | نوع الكمبيوتر: -- | السوفت وير: --", font=ctk.CTkFont(size=13), text_color="#e2e8f0")
        self.info_text.pack(anchor="w", padx=20, pady=(0, 15))

        # بطاقة خيارات التعديل
        sol_frame = ctk.CTkFrame(content, corner_radius=12, fg_color="#111a2e")
        sol_frame.pack(fill="x", pady=10, padx=10)

        sol_title = ctk.CTkLabel(sol_frame, text="اختر الحلول المراد تطبيقها على الملف (Solutions):", font=ctk.CTkFont(size=15, weight="bold"), text_color="#38bdf8")
        sol_title.pack(anchor="w", padx=20, pady=(15, 10))

        options = ["DPF", "EGR", "ADBLUE", "LAMBDA", "TVA", "EVAP", "IMMO"]
        cb_grid = ctk.CTkFrame(sol_frame, fg_color="transparent")
        cb_grid.pack(fill="x", padx=20, pady=(0, 15))

        for i, opt in enumerate(options):
            var = ctk.BooleanVar(value=(opt in ["DPF", "EGR"]))
            self.solution_vars[opt] = var
            cb = ctk.CTkCheckBox(cb_grid, text=f"{opt} OFF", variable=var, font=ctk.CTkFont(size=13))
            cb.grid(row=i // 3, column=i % 3, padx=15, pady=8, sticky="w")

        # زر المعالجة
        self.process_btn = ctk.CTkButton(content, text="⚡ تطبيق التعديل وحفظ الملف المعدل (خصم 1 نقطة)", command=self.process_file, height=50, font=ctk.CTkFont(size=16, weight="bold"), fg_color="#0284c7", hover_color="#0369a1")
        self.process_btn.pack(fill="x", padx=10, pady=(20, 10))

        self.progress_bar = ctk.CTkProgressBar(content)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.pack_forget()

    def select_file(self):
        f = filedialog.askopenfilename(filetypes=[("ECU Files", "*.bin *.ori *.hex"), ("All Files", "*.*")])
        if not f: return
        self.selected_file_path = f
        self.file_lbl.configure(text=f"الملف المحدد: {os.path.basename(f)}", text_color="#38bdf8")
        self.analyze_file(f)

    def analyze_file(self, filepath):
        self.info_text.configure(text="جاري فحص بايتات الملف والتعرف على السيارة عبر السيرفر...")
        def req():
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                with open(filepath, "rb") as bf:
                    files = {"file": (os.path.basename(filepath), bf)}
                    resp = requests.post(f"{self.server_url}/api/v1/tuning/analyze", headers=headers, files=files, timeout=30)
                data = resp.json()
                if data.get("success"):
                    brand = data.get("brand", "Generic")
                    model = data.get("model", "Vehicle")
                    ecu = data.get("ecu_type", "Standard ECU")
                    sw = data.get("sw_version", "SW_MOD")
                    txt = f"الشركة: {brand} | المحرك: {model} | الكمبيوتر: {ecu} | السوفت وير: {sw}"
                    self.after(0, lambda: self.info_text.configure(text=txt))
            except Exception as e:
                self.after(0, lambda: self.info_text.configure(text="تعذر قراءة تفاصيل الملف، ولكن يمكنك المتابعة بالتعديل"))
        threading.Thread(target=req, daemon=True).start()

    def process_file(self):
        if not self.selected_file_path:
            messagebox.showwarning("تنبيه", "يرجى اختيار ملف ECU أولاً")
            return

        selected = [opt for opt, var in self.solution_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى تحديد حل واحد على الأقل (مثل DPF أو EGR)")
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            initialfile=f"MOD_{os.path.basename(self.selected_file_path)}",
            filetypes=[("Binary File", "*.bin")]
        )
        if not out_path: return

        self.process_btn.configure(state="disabled", text="جاري التعديل بالسيرفر وخصم النقطة...")
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.start()

        def req():
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                with open(self.selected_file_path, "rb") as bf:
                    files = {"file": (os.path.basename(self.selected_file_path), bf)}
                    data_payload = {"solutions": json.dumps(selected)}
                    resp = requests.post(f"{self.server_url}/api/v1/tuning/process", headers=headers, files=files, data=data_payload, timeout=60)
                
                res_data = resp.json()
                if resp.status_code == 200 and res_data.get("success"):
                    task_id = res_data["task_id"]
                    # تنزيل الملف
                    dl_resp = requests.get(f"{self.server_url}/api/v1/tuning/download/{task_id}", headers=headers, timeout=60)
                    with open(out_path, "wb") as out_f:
                        out_f.write(dl_resp.content)

                    # تحديث الرصيد
                    me_resp = requests.get(f"{self.server_url}/api/v1/user/me", headers=headers, timeout=10)
                    if me_resp.ok:
                        self.user_data = me_resp.json()

                    self.after(0, lambda: self.process_success(out_path))
                else:
                    err_msg = res_data.get("detail", "فشل التعديل بالسيرفر")
                    self.after(0, lambda: self.process_fail(err_msg))
            except Exception as e:
                self.after(0, lambda: self.process_fail("حدث خطأ في الاتصال أثناء التعديل"))

        threading.Thread(target=req, daemon=True).start()

    def process_success(self, out_path):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.process_btn.configure(state="normal", text="⚡ تطبيق التعديل وحفظ الملف المعدل (خصم 1 نقطة)")
        self.credits_lbl.configure(text=f"الرصيد: {self.user_data.get('credits', 0)} نقطة ⚡")
        messagebox.showinfo("نجاح العملية", f"تم تعديل وحفظ الملف بنجاح في:\n{out_path}")

    def process_fail(self, msg):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.process_btn.configure(state="normal", text="⚡ تطبيق التعديل وحفظ الملف المعدل (خصم 1 نقطة)")
        messagebox.showerror("خطأ", msg)

if __name__ == "__main__":
    app = EcuClientApp()
    app.mainloop()
