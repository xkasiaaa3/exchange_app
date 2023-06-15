import requests
import customtkinter as tk
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn import linear_model
import numpy as np
from datetime import datetime, timedelta


class RadioButton(tk.CTkRadioButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class App(tk.CTk):

    def __init__(self):
        super().__init__()
        self.selected_currency = tk.StringVar()

        self.geometry("500x300")
        self.title("Kursy walut")
        self.minsize(1450, 750)

        self.label = tk.CTkLabel(master=self, text="2. Wybierz walutę", width=120, height=25, fg_color="#57c1fa",
                                 corner_radius=8)
        self.label.grid(row=0, column=3)
        self.createRadioButtons()

        self.label12 = tk.CTkLabel(master=self, text="1. Wybierz datę początkową", width=120, height=25,
                                   fg_color="#57c1fa", corner_radius=8)
        self.label12.grid(row=0, column=0, padx=25, pady=10)
        self.cal = Calendar(self, selectmode='day', year=2023, month=4, day=5)
        self.cal.grid(row=1, column=0, columnspan=2, rowspan=5, padx=50)

        self.label2 = tk.CTkLabel(master=self, text="3. Wybierz datę końcową", width=120, height=25,
                                  fg_color=("#57c1fa"), corner_radius=8)
        self.label2.grid(row=0, column=4, padx=25)
        self.cal1 = Calendar(self, selectmode='day', year=2023, month=4, day=5)
        self.cal1.grid(row=1, column=4, padx=40, columnspan=2, rowspan=5)

        self.button = tk.CTkButton(master=self, text="Sprawdź kurs", command=self.getRates, width=120, height=100)
        self.button.grid(row=1, column=6, padx=20, pady=20, rowspan=5)

    def createRadioButtons(self):
        currency = ['EUR', 'USD', 'CHF', 'GBP', 'JPY']
        for i in range(len(currency)):
            radioButton = RadioButton(self, text=currency[i], variable=self.selected_currency, value=currency[i])
            radioButton.grid(row=i+1, column=3, sticky='ns')

    def createInformation(self, rates,dates):
        date_label = tk.CTkLabel(master=self, text="Kurs "+self.selected_currency.get()+" od "+dates[0]+" do "+ dates[len(dates)-1])
        date_label.grid(row=7,column=0,columnspan=3)
        max_label = tk.CTkLabel(master=self,
                                 text="      Wartość maksymalna  " + self.selected_currency.get() + ": "+ str(max(rates))+"zł dnia: "+dates[rates.index(max(rates))])
        max_label.grid(row=8, column=0,columnspan=3,padx=20)
        min_label = tk.CTkLabel(master=self,
                                text="  Wartość minimalna  " + self.selected_currency.get() + ": " + str(
                                    min(rates)) + "zł dnia: " + dates[rates.index(min(rates))])
        min_label.grid(row=9, column=0, columnspan=3,padx=20)

        average_label = tk.CTkLabel(master=self,
                                 text="   Średnia wartość " + self.selected_currency.get() + " : "+ str(np.mean(rates))+" zł" )
        average_label.grid(row=10, column=0,columnspan=3,padx=20)




    def changeString(self, string):
        nstring = string.split('/')
        nstring1 = '20' + nstring[2] + '-' + (nstring[0] if len(nstring[0]) == 2 else '0' + nstring[0]) + '-' + (
            nstring[1] if len(nstring[1]) == 2 else '0' + nstring[1])
        return nstring1

    def plotGraph(self, rates, dates, row, column,title):
        fig = plt.figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, rates, linewidth=5, label="Wartość kursu")
        ax.set_xlabel(' ')
        plt.title(title + self.selected_currency.get())

        num_ticks = 6
        xticks = np.linspace(0, len(dates) - 1, num_ticks, dtype=int)
        xticklabels = [dates[idx] for idx in xticks]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)

        average_rate = np.mean(rates)
        average_line = [average_rate] * len(rates)
        ax.plot(dates, average_line, color='red', linestyle='--', label='Średnia')

        ax.legend()  # Add legend

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, columnspan=6,pady=50,padx=25)


    def getRates(self):
        response = requests.get(
            f"http://api.nbp.pl/api/exchangerates/rates/A/{self.selected_currency.get()}/{self.changeString(self.cal.get_date())}/{self.changeString(self.cal1.get_date())}/")
        data = response.json()['rates']
        dates = []
        rates = []
        for item in data:
            dates.append(item['effectiveDate'])
            rates.append(item['mid'])
        self.plotGraph(rates, dates, 6,0,'Kurs ')
        print("Wybrano opcję:", data)
        self.prediction(rates,dates)
        self.createInformation(rates,dates)


    def prediction(self,rates,dates):
        lastDay = datetime.strptime(dates[-1], "%Y-%m-%d")
        numeric_dates = []
        string_dates = []
        howMany = len(dates)
        print(howMany)
        for i in range(howMany):
            next_day = lastDay + timedelta(days=i+1)
            next_day_num = (next_day - datetime(1970, 1, 1)).total_seconds() / (24 * 60 * 60)
            next_day_str = next_day.strftime("%Y-%m-%d")
            numeric_dates.append(next_day_num)
            string_dates.append(next_day_str)
        y_train = np.array(rates)
        x_train = np.array(numeric_dates).reshape(-1,1)
        model = linear_model.LinearRegression()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_train)
        print(y_pred) # predicted rates
        print(string_dates) # next days
        self.plotGraph(y_pred, string_dates, 6,6,'Przewidywany kurs ')

if __name__ == "__main__":
    app = App()
    app.mainloop()