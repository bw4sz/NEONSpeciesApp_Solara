import ee
import geemap
import geemap.colormaps as cm
import numpy as np
import solara

zoom = solara.reactive(4)
center = solara.reactive([40, -100])

class Map(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data(self.selected_site.value, self.selected_year.value)
        self.add_layer_manager()
        self.add_inspector()

    def getRGB(self, year, site):
        # # Import the NEON image collection.
        start_date = ee.Date.fromYMD(year, 1, 1) 
        end_date = start_date.advance(1, "year")

        # Read in RGB NEON
        RGB = ee.ImageCollection('projects/neon-prod-earthengine/assets/DP3-30010-001').filterDate(start_date, end_date).filterMetadata('NEON_SITE', 'equals', site).first()

        return RGB

    def getCrowns(self, site):
        features = ee.FeatureCollection("users/benweinstein2010/{}".format(site))
        return features

    def getCentroid(feature):
        return feature.geometry().centroid()

    def add_ee_data(self,selected_site, year):
        # Add Earth Engine dataset

        selected_RGB = self.getRGB(year, selected_site)
        crowns = self.getCrowns(selected_site)
        empty = ee.Image()
        painted_crowns = empty.paint(**{
        'featureCollection': crowns,
        'color': 'ens_label'})
        
        # Get dictionary features
        taxonID = crowns.aggregate_array("ensembleTa").getInfo()    
        taxonID = np.unique(taxonID)
        palette = cm.get_palette("Accent", n_class=len(taxonID))
        legend_dict = {x:y for x, y in zip(taxonID, palette)}

        # Add Earth Engine layers to Map
        self.addLayer(painted_crowns, {"palette":palette, "width":1, "min":0, "max":len(taxonID)}, "Tree Species")
        self.addLayer(selected_RGB, {}, str(self.selected_site) + str(self.year))

@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        solara.Text(f"Zoom: {zoom.value}")
        solara.Text(f"Center: {center.value}")
        years = [2018, 2019, 2020, 2021, 2022]
        sites = ["BART","HARV", "OSBS"]
        selected_site = solara.reactive("BART")
        year = solara.reactive(2019)
        solara.Select(label="Site", value=selected_site, values=sites)
        solara.Select(label="Year", value=year, values=years)
                # solara components support reactive variables
        # solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
        # using 3rd party widget library require wiring up the events manually
        # using zoom.value and zoom.set
        Map.selected_site=selected_site
        Map.selected_year=year
        Map.element(  # type: ignore
            zoom=zoom.value,
            on_zoom=zoom.set,
            center=center.value,
            on_center=center.set,
            scroll_wheel_zoom=True,
            add_google_map=True,
            height="700px",
        )

