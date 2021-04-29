import plotly.express as px

class Graph():
    def __init__(self):
        pass

    def plotSurvival(self, df):
        self.fig = px.line(df, x="trial", y="survival", title='Life time of Runner')
        self.fig.add_bar(x=df['trial'], y=df['blocksize'])
        self.fig.show()