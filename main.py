import requests
import customtkinter as tk
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RadioButton(tk.CTkRadioButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class App(tk.CTk):

    def __init__(self):
        super().__init__()
        self.selected_currency = tk.StringVar()

        self.geometry("500x300")
        self.title("Kursy walut")
        self.minsize(1500, 1100)

        self.label = tk.CTkLabel(master=self, text="2. Wybierz walutę", width=120, height=25, fg_color="#57c1fa",
                                 corner_radius=8)
        self.label.grid(row=0, column=3)
        self.createRadioButtons()

        self.label12 = tk.CTkLabel(master=self, text="1. Wybierz datę początkową", width=120, height=25,
                                   fg_color="#57c1fa", corner_radius=8)
        self.label12.grid(row=0, column=0, padx=50, pady=10)
        self.cal = Calendar(self, selectmode='day', year=2023, month=4, day=5)
        self.cal.grid(row=1, column=0, columnspan=2, rowspan=5, padx=50)

        self.label2 = tk.CTkLabel(master=self, text="3. Wybierz datę końcową", width=120, height=25,
                                  fg_color=("#57c1fa"), corner_radius=8)
        self.label2.grid(row=0, column=4)
        self.cal1 = Calendar(self, selectmode='day', year=2023, month=4, day=5)
        self.cal1.grid(row=1, column=4, padx=20, columnspan=2, rowspan=5)

        self.button = tk.CTkButton(master=self, text="Sprawdź kurs", command=self.getRates, width=120, height=100)
        self.button.grid(row=1, column=6, padx=20, pady=20, rowspan=5)

    def createRadioButtons(self):
        currency = ['EUR', 'USD', 'CHF', 'GBP', 'JPY']
        for i in range(len(currency)):
            radioButton = RadioButton(self, text=currency[i], variable=self.selected_currency, value=currency[i])
            radioButton.grid(row=i+1, column=3, sticky='ns')


    def changeString(self, string):
        nstring = string.split('/')
        nstring1 = '20' + nstring[2] + '-' + (nstring[0] if len(nstring[0]) == 2 else '0' + nstring[0]) + '-' + (
            nstring[1] if len(nstring[1]) == 2 else '0' + nstring[1])
        return nstring1

    def plotGraph(self, rates, dates):
        fig = plt.figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, rates, linewidth=5)
        ax.set_xlabel(' ')
        ax.set_ylabel('Kurs '+self.selected_currency.get())
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=9, column=0, columnspan=6, pady=25, padx=50)

    def getRates(self):
        response = requests.get(
            f"http://api.nbp.pl/api/exchangerates/rates/A/{self.selected_currency.get()}/{self.changeString(self.cal.get_date())}/{self.changeString(self.cal1.get_date())}/")
        data = response.json()['rates']
        dates = []
        rates = []
        for item in data:
            dates.append(item['effectiveDate'])
            rates.append(item['mid'])
        self.plotGraph(rates, dates)
        print("Wybrano opcję:", data)


if __name__ == "__main__":
    app = App()
    app.mainloop()
