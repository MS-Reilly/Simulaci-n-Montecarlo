import random
import matplotlib.pyplot as plt
from plotly.graph_objs import Bar,Layout
from plotly import offline
from matplotlib import style
import pandas as pd
import numpy as np
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
from scipy.stats import shapiro


class Montecarlo():

    def __init__(self,num_simulaciones,num_periodos):
        #Inicialización de Yahoo finance
        style.use("ggplot")
        self.num_periodos = num_periodos
        self.num_simulaciones = num_simulaciones


        self.price_simul = []
        self.price_final = []
        yf.pdr_override()
        self.startyear = 2000
        self.startmonth = 1
        self.startday = 3
        self.get_num_freq()


        self.start = dt.datetime(int(self.startyear),int(self.startmonth),int(self.startday))
        self.now = dt.datetime.now()

        self.get_stock()

        self.randomWalk()

    def get_stock(self):
        self.stock = []
        Accion = input("Porfavor ingresar el Ticker de la acción: ")
        self.stock.append(Accion)
        self.get_data()

    def get_data(self):
        self.dataf = pdr.get_data_yahoo(self.stock,self.start,self.now,interval = self.freq)
        self.dataf = self.dataf.dropna()
        self.dataf = self.dataf.reset_index()
        print(self.dataf)
        self.dataf = self.dataf["Adj Close"]

    def get_num_freq(self):
        """Obtenemos el numero adecuado para poder dividir la frecuencia"""

        bool = True
        while bool:
            print('Eliga la frecuencia, las opciones son:  1D,5D,1WK,1MO,3MO')
            self.freq = input("Frecuencia:" )
            if self.freq == "1D":
                self.freq_num = 352
                bool = False
            elif self.freq == "5D":
                self.freq_num = 352/5
                bool = False
            elif self.freq == "1WK":
                self.freq_num = 52
                bool = False
            elif self.freq == "1MO":
                self.freq_num = 12
                bool = False
            elif self.freq == "3MO":
                self.freq_num = 4
                bool = False
            else:
                print("La frecuencia elegida no coincide con las opciones (Recuerde las mayusculas)")

    def get_return(self):
        self.retorno = self.dataf.pct_change()

    def get_daily_vol(self):
        self.daily_vol = np.std(self.retorno)

    def randomWalk(self):
        self.get_return()
        self.get_daily_vol()

        self.simulaciones =pd.DataFrame()
        lastPrice = self.dataf.iloc[-1]



        for i in range(self.num_simulaciones):
            count = 1
            self.price_simul = [lastPrice]
            self.get_daily_vol()
            price = lastPrice * (1 + np.random.normal(0,self.daily_vol))
            self.price_simul.append(price)


            for periodo in range(self.num_periodos):

                price = self.price_simul[count]*(1+np.random.normal(0,self.daily_vol))
                self.price_simul.append(price)
                count += 1
                if periodo == 251:
                    self.price_final.append(price)

            self.simulaciones[i]=self.price_simul
        print("Ok")
        self.pandas()

        fig,ax=plt.subplots()
        ax.plot(self.simulaciones)
        ax.set_title("Simulación Montercalo para el Tipo de cambio USD/MXN")
        ax.set_xlabel("Intervalo en días",fontsize=10)
        ax.set_ylabel("Tipo de Cambio")
        plt.tick_params(axis='both',which='major',labelsize=10)
        plt.show()

        fig,ax=plt.subplots()
        plt.hist(self.price_final,bins=50,density=True,color="Green",histtype='barstacked',rwidth=0.8)
        ax.set_title("Montercalo Tipo de cambio")
        ax.set_xlabel("Tipo de Cambio",fontsize=10)
        ax.set_ylabel("Frecuencia")
        plt.tick_params(axis='both',which='major',labelsize=10)

        plt.show()


    def pandas(self):
        df = pd.DataFrame(self.price_final)
        print(df.mean())
        stat,p= shapiro(df)
        print(f"El estadistico es: {stat}")
        print(f"El p value es: {p}")

        print(df.describe())


Montecarlo = Montecarlo(5000,252)
