import mapwidget.openlayers as mapwidget

import solara

zoom = solara.reactive(5)
center = solara.reactive((53.2305799, 6.5323552))


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px", "height": "500px"}):
        # solara components support reactive variables
        solara.SliderInt(label="Zoom level", value=zoom, min=1, max=20)
        # using 3rd party widget library require wiring up the events manually
        # using zoom.value and zoom.set
        mapwidget.Map.element(  # type: ignore
            zoom=zoom.value, center=center.value, height='600px', width="100%"
        )
        # solara.Text(f"Zoom: {zoom.value}")
        # solara.Text(f"Center: {center.value}")
