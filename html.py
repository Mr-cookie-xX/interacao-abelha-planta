import plotly.express as px
from jinja2 import Template

data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, x='year', y='pop')

output_html_path=r"output.html"
input_template_path = r"template.html"

plotly_jinja_data = {"fig":fig.to_html(full_html=False)}
#consider also defining the include_plotlyjs parameter to point to an external Plotly.js as described above

with open(output_html_path, "w", encoding="utf-8") as output_file:
    with open(input_template_path) as template_file:
        j2_template = Template(template_file.read())
        output_file.write(j2_template.render(plotly_jinja_data))
