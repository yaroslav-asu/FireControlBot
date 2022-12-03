from datetime import datetime
from json import load


def load_fire_data(files):
    """
    reads statistics for many periods and combines important information in dictionary
    :param files: list of tuples (getFireInformationResponse.json, getDynamicsResponse.json)
    :return: dictionary with key fireId and properties {"coordinates": {"latitude", "longitude"}, "cause",
                                                        "date_start", "date_finish", "area"}
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
                date_start = datetime.strptime(fire["extinctionTime"], "%d.%m.%Y %M:%S")

            fire_info[fire["fireIdField"]] = {"coordinates": {"latitude": coord_lat, "longitude": coord_long},
                                              "cause": fire["cause"],
                                              "date_start": date_start,
                                              "date_finish": None, "area": None}

        for fire in dynamic_resp:
            if fire_info.get(fire["fireIdField"]) is None:  # if fire missed in FireInformation
                fire_info[fire["fireIdField"]] = {"coordinates": {"latitude": None, "longitude": None},
                                                  "cause": None, "date_start": None, "date_finish": None, "area": None}

            fire_info[fire["fireIdField"]]["area"] = fire["forest"]

            date_finish = None
            if fire["detection"] is not None:
                if fire["state"] == "Локализован" and (fire_info[fire["fireIdField"]]["date_finish"] is None
                                                       or datetime.strptime(fire["detection"], "%d.%m.%Y %M:%S") >
                                                       fire_info[fire["fireIdField"]]["date_finish"]):
                    date_finish = datetime.strptime(fire["detection"], "%d.%m.%Y %M:%S")

            fire_info[fire["fireIdField"]]["date_finish"] = date_finish

    return fire_info


if __name__ == "__main__":
    print(load_fire_data([("C:/Users/artyo/Desktop/yasen_06_2022_getFireInformationResponse.json",
                           "C:/Users/artyo/Desktop/yasen_06_2022_getDynamicsResponse.json"),
                          ("C:/Users/artyo/Desktop/yasen_07_2022_getFireInformationResponse.json",
                           "C:/Users/artyo/Desktop/yasen_07_2022_getDynamicsResponse.json")]))