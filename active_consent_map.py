import json
import pandas as pd
import plotly.express as px
from urllib.request import urlopen

# Load GeoJSON of U.S. states
url = 'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json'
with urlopen(url) as response:
    geojson_data = json.load(response)

# Extract state names from the GeoJSON features
features = geojson_data['features']
state_names = [feature['properties']['name'] for feature in features]

# Create a DataFrame with state names
df = pd.DataFrame({'state': state_names})

# List of states that passed active consent legislation
active_consent_states = [
    "Florida", "Idaho", "Iowa", "Kentucky", "Louisiana", 
    "Nevada", "New Hampshire", "North Carolina", 
    "Ohio", "Tennessee", "Texas"
]

# Bill name and year per state
hover_text = {
    "Ohio": "House Bill 8 (2025)",
    "Idaho": "Title 32 (2024)",
    "North Carolina": "Senate Bill 49 (2023)",
    "Florida": "House Bill 241 (2021)",
    "Texas": "Senate Bill 9 (2021)",
    "Tennessee": "Senate Bill 1443 (2023)",
    "Kentucky": "Senate Bill 150.132 (2023)",
    "Iowa": "Senate File 496 (2023)",
    "Nevada": "NRS 389 (2024)",
    "New Hampshire": "RSA 186:11 (2023)",
    "Louisiana": "Act 837"
}

# Add consent law status
df["consent_law"] = df["state"].apply(lambda x: "Passed" if x in active_consent_states else "—")

# Build hover text (state name + law info)
df["hover_text"] = df["state"].apply(
    lambda x: f"{x}<br>{hover_text[x]}" if x in hover_text else x
)

# Create the choropleth map
fig = px.choropleth(
    data_frame=df,
    geojson=geojson_data,
    locations="state",
    featureidkey="properties.name",
    color="consent_law",
    color_discrete_map={
        "Passed": "#FF7043",
        "—": "#E0E0E0"
    },
    scope="usa",
    hover_name="hover_text",  # <- Custom hover content here
    hover_data={"consent_law": False, "state": False},
    title="U.S. States with Active Consent Legislation (Past 5 Years)"
)

# Update the layout for better appearance
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

# Display the figure
fig.show()

# Optional: Save the figure as an HTML file
fig.write_html("C:/Users/ulyss/Documents/Coding/Actionaly Map/active_consent_map.html")
