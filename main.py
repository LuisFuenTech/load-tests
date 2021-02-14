import subprocess
import os
import pandas
import numpy
from tkinter import scrolledtext, messagebox, ttk, PhotoImage
from utils.regression import *
from utils.clustering import *

request_types = ["Secuencial", "Concurrente"]
total_of_clusters = ["2", "3"]
cluster_object = Cluster()
regression_object = Regression()

def process():
    results_text_area.delete("1.0", tk.END)
    report_text_area.delete("1.0", tk.END)
    if (str(url_input.get()) == "" or str(total_of_request_input.get()) == ""):
        print(tk.messagebox.showinfo(
            message="¡Debe ingresar todos los datos!", title="Alerta"))
    else:
        try:
            process_request_type(combo_box_request.get())
        except ValueError:
            print(tk.messagebox.showinfo(
                message="Error en número de peticiones!", title="Alerta"))


def process_request_type(request_name):

    url_to_process = url_input.get().lower()
    number_of_requests = total_of_request_input.get()

    if(url_to_process.find("/", -1) == -1):
        url_to_process += "/"

    progress_bar = ttk.Progressbar(data_tab, mode="indeterminate")
    progress_bar.place(x=220, y=120, width=200)
    progressbar_text = tk.Label(
        data_tab, text="Procesando petición...")
    progressbar_text.place(x=260, y=140)

    try:
        if(request_name == request_types[0]):
            ab_process = subprocess.Popen("ab -n {requests} -e reporte.csv {url}".format(requests=number_of_requests, url=url_to_process), shell=True,
                                          stdout=subprocess.PIPE, universal_newlines=True)
        else:
            ab_process = subprocess.Popen("ab -n {requests} -c {requests} -e reporte.csv {url}".format(requests=number_of_requests, url=url_to_process), shell=True,
                                          stdout=subprocess.PIPE, universal_newlines=True)

        progress_bar.start(18)

        while ab_process.poll() is None:
            data_tab.update()

        progress_bar.stop()
        progress_bar.destroy()
        progressbar_text.destroy()
        process_response = ab_process.communicate()[0]

        if (process_response == ""):
            print(tk.messagebox.showinfo(
                message="URL incorrecta!", title="Alerta"))
        else:
            results_text_area.delete("1.0", tk.END)
            results_text_area.insert(tk.END, process_response)
            report_text_area.delete("1.0", tk.END)
            datos = pandas.read_csv("reporte.csv", names=[
                "%", "ms"], delimiter=",", header=0)
            #print(datos)
            datos = datos.drop([95, 96, 97, 98, 99])
            pandas.set_option('display.max_rows',
                              datos.shape[0] + 1)
            report_text_area.insert(tk.END, datos)

            if(request_name == request_types[0]):
                cluster_object.process_clustering(datos, str(combo_box_clusters.get()), main_graphics_tab, cluster_frame)
            else:
                regression_object.process_regression(datos, regression_frame, main_graphics_tab)

            main_data_tab.tab(1, state='normal')
    except Exception as e:
        print(e)
        print(tk.messagebox.showinfo(
            message="¡No se puedo procesar la url!", title="Alerta"))


def centroids():
    centr = cluster_object.centroids
    cade = ""
    for i, val in enumerate(centr):
        cade += "Centroide {number} [{coordinates}] \n".format(
            number=i+1, coordinates=listToString(numpy.round(val, 2)))
    tk.messagebox.showinfo(message=cade, title="Centroides")


def listToString(list):
    newString = ""

    for item in list:
        newString += str(item) + ', '

    return newString[0:len(newString)-2]


def combo_event():
    if (combo_box_request.get() == request_types[0]):
        combo_box_clusters.configure(None, state="readonly")
    else:
        combo_box_clusters.configure(None, state="disabled")

icon = os.getcwd() + '/test.png'

app = tk.Tk()
app.title("Pruebas de carga")
app.eval('tk::PlaceWindow . center')
app.iconphoto(True, PhotoImage(file=os.getcwd()+'/test.png'))
app.geometry("735x530")

main_data_tab = ttk.Notebook(app)
data_tab = ttk.Frame(main_data_tab)
graphics_tab = ttk.Frame(main_data_tab)
main_data_tab.add(data_tab, text='Datos')
main_data_tab.add(graphics_tab, text='Gráficas')
main_data_tab.pack(expand=1, fill="both")

main_graphics_tab = ttk.Notebook(graphics_tab)
regression_frame = ttk.Frame(main_graphics_tab)
cluster_frame = ttk.Frame(main_graphics_tab)
main_graphics_tab.add(regression_frame, text='Regresión')
main_graphics_tab.add(cluster_frame, text='Clusters')
main_graphics_tab.pack(expand=1, fill="both")

tk.Label(data_tab, text="PRUEBAS DE CARGA").place(x=325, y=10)

tk.Label(data_tab, text="Tipo de petición").place(x=350, y=35)
combo_box_request = ttk.Combobox(
    data_tab, state="readonly", width=14, values=request_types)
combo_box_request.bind("<<ComboboxSelected>>", lambda _: combo_event())
combo_box_request.grid(column=1, row=1)
combo_box_request.place(x=350, y=60)
combo_box_request.current(0)

tk.Label(data_tab, text="Total de clusters").place(x=490, y=35)
combo_box_clusters = ttk.Combobox(data_tab, state="readonly", width=14,
                                  values=total_of_clusters)
combo_box_clusters.grid(column=1, row=1)
combo_box_clusters.place(x=490, y=60)
combo_box_clusters.current(0)

tk.Label(data_tab, text="Peticiones").place(x=50, y=90)
total_of_request_input = tk.Entry(data_tab, width=8, text="")
total_of_request_input.place(x=50, y=115)
total_of_request_input.insert(tk.END, "")

tk.Label(data_tab, text="URL").place(x=50, y=35)
url_input = tk.Entry(data_tab, width=33, text="")
url_input.place(x=50, y=60)
url_input.insert(tk.END, "")

process_button = tk.Button(
    cluster_frame, command=centroids, text="Mostrar centroides")
process_button.place(x=73, y=5)

process_button = tk.Button(data_tab, command=process, text="Procesar")
process_button.place(x=125, y=110)

tk.Label(data_tab, text="Reporte").place(x=50, y=165)
report_text_area = tk.scrolledtext.ScrolledText(data_tab, width=25, height=15)
report_text_area.place(x=50, y=195)

tk.Label(data_tab, text="Resultados").place(x=300, y=165)
results_text_area = tk.scrolledtext.ScrolledText(data_tab, width=45, height=15)
results_text_area.place(x=300, y=195)

main_data_tab.tab(1, state='disabled')

tk.mainloop()
