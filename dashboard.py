import pandas as pd
import plotly.express as px

def sector_dashboard():
    data = {
        "Sector": ["IT", "Banking", "Energy", "Pharma"],
        "Sentiment Score": [78, 62, 55, 70]
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x="Sector", y="Sentiment Score")
    return fig
