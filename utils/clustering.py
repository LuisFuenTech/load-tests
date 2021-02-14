from matplotlib import pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans


class Cluster():

    def __init__(self):
        self.graphic_tab = ""
        self.cluster = ""
        self.centroids = ""

    def process_clustering(self, data, cluster_value, graphic_tab, cluster):
        self.graphic_tab = graphic_tab
        self.cluster = cluster

        data_array = data.values
        x = data_array[:, 0:1]
        y = data_array[:, 1:2]

        if (cluster_value == "2"):
            kmeans = KMeans(n_clusters=2)
            kmeans.fit(data_array)
        else:
            kmeans = KMeans(n_clusters=3)
            kmeans.fit(data_array)

        self.centroids = kmeans.cluster_centers_
        self.graphic_clusters(x, y, kmeans)
        return kmeans.cluster_centers_

    def graphic_clusters(self, x, y, kmeans):
        self.graphic_tab.tab(0, state='disabled')
        self.graphic_tab.tab(1, state='normal')
        self.graphic_tab.select(1)
        fig = plot.figure(figsize=(6.5, 4))
        axies = fig.gca()
        plot.scatter(x.reshape(x.shape[0]), y.reshape(
            y.shape[0]), s=11, c=kmeans.labels_, cmap="rainbow")
        centers = kmeans.cluster_centers_
        
        plot.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=0.5)
        plot.ylabel('Tiempo (ms)')
        plot.xlabel('Porcentajes (%)')
        
        canvas = FigureCanvasTkAgg(fig, master=self.cluster)
        plot_widget = canvas.get_tk_widget()
        plot_widget.place(x=75, y=45)
