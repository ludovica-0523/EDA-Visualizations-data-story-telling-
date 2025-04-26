
# Save this as app.py inside Jupyter
from flask import Flask, render_template_string, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Step 1: Fake simple climate change dataset
data = {
    'Country': ['USA', 'USA', 'India', 'India', 'Germany', 'Germany'],
    'Year': [2020, 2021, 2020, 2021, 2020, 2021],
    'CO2 Emissions': [5000, 5100, 3000, 3200, 2000, 1900]  # simple numbers
}
df = pd.DataFrame(data)

# Step 2: Homepage with a dropdown
html_template = '''
<!doctype html>
<html>
<head>
    <title>Climate Change Data</title>
</head>
<body>
    <h1>Climate Change Visualization</h1>
    <form method="post">
        <label for="country">Choose a country:</label>
        <select name="country" id="country">
            {% for country in countries %}
            <option value="{{country}}">{{country}}</option>
            {% endfor %}
        </select>
        <button type="submit">Show Data</button>
    </form>

    {% if plot %}
    <div>{{plot | safe}}</div>
    {% endif %}
</body>
</html>
'''

# Step 3: Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    plot = None
    countries = df['Country'].unique()

    if request.method == 'POST':
        selected_country = request.form['country']
        filtered_df = df[df['Country'] == selected_country]

        fig = px.line(filtered_df, x='Year', y='CO2 Emissions', title=f'CO2 Emissions for {selected_country}')
        plot = fig.to_html(full_html=False)

    return render_template_string(html_template, countries=countries, plot=plot)

# Step 4: Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
