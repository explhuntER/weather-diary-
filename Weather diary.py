# weather_diary.py
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary / Дневник погоды")
        self.root.geometry("800x500")
        
        self.entries = []  # список всех записей
        self.filename = "weather_data.json"
        self.load_from_file(self.filename)  # загружаем при старте
        
        self.create_widgets()
        self.update_table()
    
    def create_widgets(self):
        # === Панель ввода ===
        input_frame = ttk.LabelFrame(self.root, text="Добавить запись", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Температура
        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Описание
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        
        # Осадки
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Кнопка добавления
        ttk.Button(input_frame, text="➕ Добавить запись", command=self.add_entry).grid(row=2, column=2, columnspan=2, pady=5)
        
        # === Панель фильтрации ===
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=12)
        self.filter_date.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Температура >").grid(row=0, column=2, padx=5, pady=5)
        self.filter_temp = ttk.Entry(filter_frame, width=6)
        self.filter_temp.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(filter_frame, text="°C").grid(row=0, column=4, padx=5, pady=5)
        
        ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter).grid(row=0, column=5, padx=10, pady=5)
        ttk.Button(filter_frame, text="❌ Сбросить фильтр", command=self.reset_filter).grid(row=0, column=6, padx=5, pady=5)
        
        # === Таблица записей ===
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("#", "Дата", "Температура (°C)", "Описание", "Осадки")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Настройка заголовков
        self.tree.heading("#", text="№")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Температура (°C)", text="Температура (°C)")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")
        
        self.tree.column("#", width=40, anchor="center")
        self.tree.column("Дата", width=100, anchor="center")
        self.tree.column("Температура (°C)", width=100, anchor="center")
        self.tree.column("Описание", width=300)
        self.tree.column("Осадки", width=60, anchor="center")
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # === Кнопки управления файлами ===
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(btn_frame, text="💾 Сохранить в JSON", command=self.save_to_file).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📂 Загрузить из JSON", command=self.load_from_file_dialog).pack(side="left", padx=5)
    
    def add_entry(self):
        """Добавление записи с проверкой"""
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = "Да" if self.precip_var.get() else "Нет"
        
        # Валидация
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return
        
        try:
            temp_val = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return
        
        if not description:
            messagebox.showerror("Ошибка", "Описание не может быть пустым")
            return
        
        # Добавляем запись
        self.entries.append({
            "date": date,
            "temperature": temp_val,
            "description": description,
            "precipitation": precipitation
        })
        
        # Очищаем поля
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
        
        self.update_table()
        messagebox.showinfo("Успех", "Запись добавлена")
    
    def update_table(self, filtered_entries=None):
        """Обновление таблицы"""
        # Удаляем все строки
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        data = filtered_entries if filtered_entries is not None else self.entries
        
        for idx, entry in enumerate(data, start=1):
            self.tree.insert("", "end", values=(
                idx,
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
    
    def apply_filter(self):
        """Фильтрация записей"""
        filter_date = self.filter_date.get().strip()
        filter_temp_str = self.filter_temp.get().strip()
        
        filtered = self.entries.copy()
        
        # Фильтр по дате
        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [e for e in filtered if e["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты фильтра")
                return
        
        # Фильтр по температуре (> значение)
        if filter_temp_str:
            try:
                temp_threshold = float(filter_temp_str)
                filtered = [e for e in filtered if e["temperature"] > temp_threshold]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура фильтра должна быть числом")
                return
        
        self.update_table(filtered)
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.update_table()
    
    def save_to_file(self, filename=None):
        """Сохранение в JSON"""
        if filename is None:
            filename = self.filename
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_from_file(self, filename):
        """Загрузка из JSON"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.entries = []
    
    def load_from_file_dialog(self):
        """Загрузка через диалог"""
        filename = filedialog.askopenfilename(
            title="Выберите JSON файл",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.load_from_file(filename)
            self.update_table()
            messagebox.showinfo("Успех", f"Загружено из {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()