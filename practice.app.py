
from flask import Flask, render_template_string, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Example Surface Temperature Data
data = {
    "Region": ["Global", "Global", "Global", 
               "Northern Hemisphere", "Northern Hemisphere", "Northern Hemisphere", 
               "Southern Hemisphere", "Southern Hemisphere", "Southern Hemisphere"],
    "Year": [2000, 2010, 2020, 
             2000, 2010, 2020, 
             2000, 2010, 2020],
    "Surface_Temp_Anomaly": [0.42, 0.72, 1.02, 0.48, 0.85, 1.18, 0.37, 0.59, 0.86]
}
df = pd.DataFrame(data)

# HTML Template inside Python
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Surface Temperature Anomalies</title>
</head>
<body>
    <h1>Surface Temperature Anomalies</h1>
    <form method="POST">
        <label>Select Region:</label><br>
        <select name="region">
            {% for r in regions %}
            <option value="{{r}}" {% if r == selected_region %}selected{% endif %}>{{r}}</option>
            {% endfor %}
        </select><br><br>
        
        <label>Choose Year Range:</label><br>
        <input type="number" name="year_start" value="{{year_start or ''}}" placeholder="Start Year"><br>
        <input type="number" name="year_end" value="{{year_end or ''}}" placeholder="End Year"><br><br>
        
        <button type="submit">Update Graph</button>
    </form>

    <div>
        {{plot_div|safe}}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_region = "Global"
    year_start = 2000
    year_end = 2020

    if request.method == 'POST':
        selected_region = request.form.get('region')
        year_start = int(request.form.get('year_start', 2000))
        year_end = int(request.form.get('year_end', 2020))

    # Filter data based on selection
    dff = df[(df["Region"] == selected_region) & 
             (df["Year"] >= year_start) & 
             (df["Year"] <= year_end)]

    # Color map based on region
    color_map = {
        "Global": "blue",
        "Northern Hemisphere": "red",
        "Southern Hemisphere": "green"
    }

    # Create Plotly figure
    fig = px.line(dff, x="Year", y="Surface_Temp_Anomaly",
                  title=f"Surface Temperature Anomaly in {selected_region} (°C)",
                  line_shape="spline")
    fig.update_traces(line=dict(color=color_map.get(selected_region, 'black'), width=4))
    fig.update_layout(
        yaxis_title="Temperature Anomaly (°C)",
        plot_bgcolor="white",  # background white
        paper_bgcolor="white"  # outer background white
    )
    plot_div = fig.to_html(full_html=False)

    regions = df["Region"].unique()
    return render_template_string(html, plot_div=plot_div, regions=regions,
                                  selected_region=selected_region,
                                  year_start=year_start, year_end=year_end)

if __name__ == '__main__':
    app.run(debug=True, port=5020)


