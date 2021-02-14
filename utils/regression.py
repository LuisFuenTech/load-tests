import tkinter as tk

from matplotlib import pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class Regression():

    def __init__(self):
        self.graphic_tab = ""
        self.regression = ""

    def process_regression(self, data, regression, graphic_tab):
        self.graphic_tab = graphic_tab
        self.regression = regression

        data_array = data.values
        x_reg = data_array[:, 0:1]
        y_reg = data_array[:, 1:2]
        test_size = 0.2
        seed = 1234
        x_train, x_test, y_train, y_test = train_test_split(
            x_reg.reshape(-1, 1), y_reg.reshape(-1, 1), test_size=test_size, random_state=seed)
        model = LinearRegression()
        model.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))

        if (model.intercept_ > 0):
            y_cad = "Y = {y} X + {x}".format(
                y=round(model.coef_[0].item(), 3), x=round(model.intercept_.item(), 3))
        else:
            y_cad = "Y = {y} X - {x}".format(
                y=round(model.coef_[0].item(), 3), x=round(model.intercept_.item(), 3))

        tk.Label(regression, text="Ecuación de regresión").place(x=75, y=25)
        tk.Label(regression, text=y_cad).place(x=230, y=25)

        self.graphic_regression(
            x_train.reshape(-1, 1), y_train.reshape(-1, 1), x_reg.reshape(-1, 1), model)

    def graphic_regression(self, x_train, y_train, x_reg, model):
        self.graphic_tab.tab(1, state='disabled')
        self.graphic_tab.tab(0, state='normal')
        self.graphic_tab.select(0)
        
        figure = plot.figure(figsize=(6.3, 4))
        plot.scatter(x_train, y_train, s=10)
        x_min = x_reg.min()
        x_max = x_reg.max()
        y_min = (model.coef_ * x_min) + model.intercept_
        y_max = (model.coef_ * x_max) + model.intercept_
        plot.plot([x_min, x_max], [y_min.item(), y_max.item()], color='r')
        plot.xlabel('Porcentaje (%)')
        plot.ylabel('Tiempo (ms)')
        canvas = FigureCanvasTkAgg(figure, master=self.regression)
        plot_widget = canvas.get_tk_widget()
        plot_widget.place(x=75, y=45)
