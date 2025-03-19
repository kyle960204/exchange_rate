import tkinter as tk #GUI工具包
from tkinter import ttk
import requests
from datetime import datetime

# 設定 API Key（請替換為你自己的 API Key）
API_KEY = "1d9a5f151db38be79143f138"  
# 需要去 exchangerate-api.com 註冊獲取
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("即時匯率轉換器")
        self.root.geometry("500x400")

        # 獲取匯率數據
        self.currencies = self.get_currencies()
        self.exchange_rates = {}
        self.update_rates("TWD")  # 預設基底貨幣為台幣

        # 建立介面
        self.create_widgets()

    def get_currencies(self):
        # 這裡可以從 API 獲取所有支援的貨幣，這裡先列出常見貨幣
        return ["TWD", "USD", "EUR", "JPY", "CNY", "HKD", "GBP", "AUD"]

    def update_rates(self, base_currency):
        try:
            response = requests.get(BASE_URL + base_currency)
            data = response.json()
            if data["result"] == "success":
                self.exchange_rates = data["conversion_rates"]
                self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                self.exchange_rates = {}
                self.last_updated = "無法獲取數據"
        except Exception as e:
            print(f"錯誤: {e}")
            self.exchange_rates = {}
            self.last_updated = "無法獲取數據"

    def create_widgets(self):
        # 標題
        title_label = tk.Label(self.root, text="即時匯率轉換器", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # 選擇貨幣框架
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # 選擇來源貨幣
        tk.Label(frame, text="來源貨幣:").grid(row=0, column=0, padx=5)
        self.from_currency = ttk.Combobox(frame, values=self.currencies, state="readonly")
        self.from_currency.grid(row=0, column=1, padx=5)
        self.from_currency.set("TWD")

        # 選擇目標貨幣
        tk.Label(frame, text="目標貨幣:").grid(row=1, column=0, padx=5)
        self.to_currency = ttk.Combobox(frame, values=self.currencies, state="readonly")
        self.to_currency.grid(row=1, column=1, padx=5)
        self.to_currency.set("USD")

        # 輸入金額
        tk.Label(frame, text="金額:").grid(row=2, column=0, padx=5)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=2, column=1, padx=5)
        self.amount_entry.insert(0, "100")

        # 顯示結果
        self.result_label = tk.Label(self.root, text="結果: ", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # 顯示即時匯率與現金匯率
        self.rate_label = tk.Label(self.root, text="即時匯率: 等待計算\n現金匯率: 等待計算", font=("Arial", 10))
        self.rate_label.pack(pady=5)

        # 最後更新時間
        self.time_label = tk.Label(self.root, text=f"最後更新: {self.last_updated}", font=("Arial", 10))
        self.time_label.pack(pady=5)

        # 轉換按鈕
        convert_button = tk.Button(self.root, text="轉換", command=self.convert)
        convert_button.pack(pady=10)

        # 更新匯率按鈕
        update_button = tk.Button(self.root, text="更新匯率", command=lambda: self.update_rates(self.from_currency.get()))
        update_button.pack(pady=5)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            # 更新匯率（如果需要）
            if from_curr != list(self.exchange_rates.keys())[0]:
                self.update_rates(from_curr)

            # 計算即時匯率
            spot_rate = self.exchange_rates.get(to_curr, 0)
            if spot_rate == 0:
                self.result_label.config(text="錯誤: 無法獲取匯率")
                return

            # 假設現金匯率為即時匯率的 98%
            cash_rate = spot_rate * 0.98

            # 計算轉換後金額
            converted_amount_spot = amount * spot_rate
            converted_amount_cash = amount * cash_rate

            # 更新顯示
            self.result_label.config(text=f"結果: {amount:.2f} {from_curr} = {converted_amount_spot:.2f} {to_curr} (即時)\n"
                                         f"      {amount:.2f} {from_curr} = {converted_amount_cash:.2f} {to_curr} (現金)")
            self.rate_label.config(text=f"即時匯率: 1 {from_curr} = {spot_rate:.4f} {to_curr}\n"
                                       f"現金匯率: 1 {from_curr} = {cash_rate:.4f} {to_curr}")
            self.time_label.config(text=f"最後更新: {self.last_updated}")

        except ValueError:
            self.result_label.config(text="錯誤: 請輸入有效的金額")
        except Exception as e:
            self.result_label.config(text=f"錯誤: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
