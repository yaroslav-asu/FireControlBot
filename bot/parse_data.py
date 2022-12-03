from datetime import datetime
from json import load
from pprint import pprint


def load_fire_data(files):
    """
    reads statistics for many periods and combines important information in dictionary
    :param files: list of tuples (getFireInformationResponse.json, getDynamicsResponse.json)
    :return: dictionary with key fireId and properties {"coordinates": {"latitude", "longitude"}, "cause",
                                                        "municipality", "date_start", "date_finish", "area"}
    """
    fire_info = dict()

    for period in files:
        with open(period[0], "r", encoding="utf-8") as file:
            fire_information_resp = load(file)[0]["Body"]["getFireInformationResponse"]
            fire_information_resp = fire_information_resp["MessageData"]["AppData"]["data"]
        with open(period[1], "r", encoding="utf-8") as file:
            dynamic_resp = load(file)[0]["Body"]["getDynamicsResponse"]["MessageData"]["AppData"]["data"]

        for fire in fire_information_resp:
            # converting coordinates into decimal form
            coord_lat = fire["latitude"]["degree"] + \
                        (fire["latitude"]["minute"] / 60) + (fire["latitude"]["second"] / 3600)
            coord_long = fire["longitude"]["degree"] + \
                         (fire["longitude"]["minute"] / 60) + (fire["longitude"]["second"] / 3600)

            if fire["extinctionTime"] is None:
                date_start = None
            else:
                date_start = datetime.strptime(fire["extinctionTime"], "%d.%m.%Y %H:%M")

            fire_info[fire["fireIdField"]] = {"coordinates": {"latitude": coord_lat, "longitude": coord_long},
                                              "cause": fire["cause"], "municipality": fire["municipality"],
                                              "date_start": date_start,
                                              "date_finish": None, "area": None}

        for fire in dynamic_resp:
            if fire_info.get(fire["fireIdField"]) is None:  # if fire missed in FireInformation
                fire_info[fire["fireIdField"]] = {"coordinates": {"latitude": None, "longitude": None},
                                                  "municipality": None, "cause": None,
                                                  "date_start": None, "date_finish": None, "area": None}

            fire_info[fire["fireIdField"]]["area"] = fire["forest"]

            date_finish = None
            if fire["detection"] is not None:
                if fire["state"] == "Ликвидирован":
                    date_finish = datetime.strptime(fire["detection"], "%d.%m.%Y %H:%M")

            fire_info[fire["fireIdField"]]["date_finish"] = date_finish

    return fire_info


if __name__ == "__main__":
    pprint(load_fire_data([("./extra_data/yasen_06_2022_getFireInformationResponse.json",
                           "./extra_data/yasen_06_2022_getDynamicsResponse.json"),
                          ("./extra_data/yasen_07_2022_getFireInformationResponse.json",
                           "./extra_data/yasen_07_2022_getDynamicsResponse.json")]))
