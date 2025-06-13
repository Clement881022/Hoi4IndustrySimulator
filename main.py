import globals
from civilian_factory_line import CivilianFactoryLine
from military_factory_line import MilitaryFactoryLine
from event_system import EventManager
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

event_manager = EventManager()
ic_values = []
dates = []

while(globals.TRANSFORM_DATE < globals.END_DATE):
    globals.reset()
    globals.TRANSFORM_DATE += relativedelta(months=1)
    civilian_factory_line = CivilianFactoryLine(event_manager)
    military_factory_line = MilitaryFactoryLine(event_manager)
    while globals.CURRENT_DATE < globals.END_DATE:  
        civilian_factory_line.build_one_day()
        military_factory_line.produce_one_day()
        globals.CURRENT_DATE += timedelta(days=1)
    print(f"民轉軍時間: {globals.TRANSFORM_DATE.date()} 可用民:{civilian_factory_line.active_civilian_num} 民工數: {globals.CIVILIAN} 軍工數: {globals.MILITARY} 總產能: {military_factory_line.ic}")
    ic_values.append(military_factory_line.ic)
    dates.append(globals.TRANSFORM_DATE.date())

plt.figure(figsize=(10, 6))  # 設定圖形大小
plt.plot(dates, ic_values, marker='o', color='b', label='ic')  # 繪製折線圖
plt.xlabel('switch mil time', fontsize=12)  # X軸標籤
plt.ylabel('ic', fontsize=12)  # Y軸標籤
plt.title('ic change', fontsize=14)  # 標題
plt.xticks(rotation=45)  # 讓X軸標籤傾斜45度，避免擁擠
plt.legend()  # 顯示圖例
plt.grid(True)  # 顯示格線
plt.tight_layout()  # 自動調整佈局
plt.show()  # 顯示圖形
