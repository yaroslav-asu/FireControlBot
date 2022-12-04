import time
from datetime import datetime
from pprint import pprint

import pandas as pd
import plotly.express as px
from dotenv import dotenv_values
from bot.core.config import *

from bot.parse_data import load_fire_data


def generate_heatmap():
    today = datetime.today()
    quakes = list(filter(lambda y: y['Площадь'] and y['latitude'] and y['longitude'],
                         map(lambda x: {'latitude': x['coordinates']['latitude'],
                                        'longitude': x['coordinates']['longitude'],
                                        'Площадь': x['area']},
                             filter(lambda x: x['date_start'] and x['date_start'] and x['date_start'] and x[
                                 'date_start'].year == today.year,
                                    load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                                                     "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                                                    ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                                                     "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")]).values()))))

    px.set_mapbox_access_token(
        config['TOKEN_MAPBOX']
    )

    fig = px.density_mapbox(quakes, lat="latitude", lon="longitude", z='Площадь', zoom=4, width=830, height=600,
                            center=dict(lat=62, lon=72.3),
                            color_continuous_scale=[(0, "yellow"), (0.5, "orange"), (1, "red")],
                            )

    fig.update_layout(
        mapbox_style="mapbox://styles/yaroslav-asu/clb8e2nsa004n15oh1gge3igm"
    )
    fig.write_image("bot/heatmap/year.png")


def show_heat_map(message, period: str):
    bot.send_message(message.chat.id, 'Пожалуйста, подождите, идет загрузка карты')
    time.sleep(0.5)
    bot.send_photo(message.chat.id, photo=open(f'bot/heatmap/{period}.png', 'rb'))


if __name__ == "__main__":
    generate_heatmap()
