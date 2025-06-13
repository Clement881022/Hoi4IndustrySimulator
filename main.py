# main.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import globals
from civilian_factory_line import CivilianFactoryLine
from military_factory_line import MilitaryFactoryLine
from event_system import EventManager
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.entries_info = [
            ("模擬結束時間 END_DATE (yyyy-mm-dd)", "END_DATE", globals.END_DATE.date(), "date"),
            ("裝備研究完成時間 TARGET_TECH_DATE (yyyy-mm-dd)", "TARGET_TECH_DATE", globals.TARGET_TECH_DATE.date(), "date"),
            ("初始民工 CIVILIAN", "CIVILIAN", globals.CIVILIAN, "int"),
            ("初始軍工 MILITARY", "MILITARY", globals.MILITARY, "int"),
            ("消費品比例 CONSUMER_GOODS", "CONSUMER_GOODS", globals.CONSUMER_GOODS, "float"),
            ("民轉軍價格 CIVILIAN_TO_MILITARY_COST", "CIVILIAN_TO_MILITARY_COST", globals.CIVILIAN_TO_MILITARY_COST, "int"),
            ("額外建築加成 ADDITIONAL_CONSTRUCTION_SPEED", "ADDITIONAL_CONSTRUCTION_SPEED", globals.ADDITIONAL_CONSTRUCTION_SPEED, "float"),
            ("每軍工貿易外流民工 TRADE_CIV_EACH_MIL", "TRADE_CIV_EACH_MIL", globals.TRADE_CIV_EACH_MIL, "float"),
        ]

        self.entries = {}
        for idx, (label, var_name, default_value, _) in enumerate(self.entries_info):
            tk.Label(root, text=label).grid(row=idx, column=0, sticky="e", pady=2)
            entry = tk.Entry(root)
            entry.insert(0, str(default_value))
            entry.grid(row=idx, column=1, pady=2)
            self.entries[var_name] = entry
        self.root.title("Hoi4IndustrySimulator")

        # 模式下拉式選單
        tk.Label(root, text="模擬模式").grid(row=len(self.entries_info), column=0, sticky="e")
        self.mode_var = tk.StringVar(value="CivToMil")
        self.mode_menu = ttk.Combobox(root, textvariable=self.mode_var, values=["CivToMil", "MilOnly"], state="readonly")
        self.mode_menu.grid(row=len(self.entries_info), column=1)
        self.start_button = tk.Button(root, text="開始模擬", command=self.run_simulation)
        self.start_button.grid(row=len(self.entries_info)+1, column=0, columnspan=2, pady=10)

        # Matplotlib 圖表區域
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=20, padx=10, pady=10)

    def run_simulation(self):
        globals.SWITCH_DATE = datetime(1938, 1, 1)
        globals.TRANSFORM_DATE = datetime(1938, 1, 1)
        globals.CURRENT_DATE = datetime(1936, 1, 1)
        try:
            for label, var_name, _, var_type in self.entries_info:
                text = self.entries[var_name].get()
                if var_type == "int":
                    setattr(globals, var_name, int(text))
                elif var_type == "float":
                    setattr(globals, var_name, float(text))
                elif var_type == "date":
                    setattr(globals, var_name, datetime.strptime(text, "%Y-%m-%d"))
        except Exception as e:
            messagebox.showerror("錯誤", f"參數錯誤：{e}")
            return

        event_manager = EventManager()
        ic_values = []
        dates = []
        if self.mode_var.get() == "CivToMil":
            while globals.TRANSFORM_DATE < globals.END_DATE:
                globals.CIVILIAN = int(self.entries["CIVILIAN"].get())
                globals.MILITARY = int(self.entries["MILITARY"].get())
                globals.CURRENT_DATE = datetime(1936, 1, 1)
                globals.TRANSFORM_DATE += relativedelta(months=1)
                civilian_factory_line = CivilianFactoryLine(event_manager)
                military_factory_line = MilitaryFactoryLine(event_manager)

                while globals.CURRENT_DATE < globals.END_DATE:
                    civilian_factory_line.build_one_day()
                    military_factory_line.produce_one_day()
                    globals.CURRENT_DATE += timedelta(days=1)

                ic_values.append(military_factory_line.ic)
                dates.append(globals.TRANSFORM_DATE.date())
        else:
            globals.SWITCH_DATE = datetime(1936, 1, 1)
            globals.TRANSFORM_DATE = datetime(1999, 1, 1)
            while globals.SWITCH_DATE < globals.END_DATE:
                globals.CIVILIAN = int(self.entries["CIVILIAN"].get())
                globals.MILITARY = int(self.entries["MILITARY"].get())
                globals.CURRENT_DATE = datetime(1936, 1, 1)
                globals.SWITCH_DATE += relativedelta(months=1)
                civilian_factory_line = CivilianFactoryLine(event_manager)
                military_factory_line = MilitaryFactoryLine(event_manager)

                while globals.CURRENT_DATE < globals.END_DATE:
                    civilian_factory_line.build_one_day()
                    military_factory_line.produce_one_day()
                    globals.CURRENT_DATE += timedelta(days=1)

                ic_values.append(military_factory_line.ic)
                dates.append(globals.SWITCH_DATE.date())

        # 畫圖到 tkinter 中
        self.ax.clear()
        self.ax.plot(dates, ic_values, marker='o', color='b', label='ic')
        self.ax.set_title("ic change")
        self.ax.set_xlabel("SwitchMilDate" if self.mode_var.get() == "MilOnly" else "CivToMilDate")
        self.ax.set_ylabel("ic")
        self.ax.legend()
        self.ax.grid(True)
        self.figure.autofmt_xdate()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
