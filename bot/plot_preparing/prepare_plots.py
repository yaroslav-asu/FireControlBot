from bot.parse_data import load_fire_data
from datetime import timedelta, date, datetime
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

fire_data = load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                             "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                            ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                             "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")])


def date_iterator(date_start, date_finish):
    """
    generator for dates in range
    :param date_start: beginning
    :param date_finish: ending
    """
    for i in range(int((date_finish - date_start).days + 1)):
        yield date_start + timedelta(i)


def get_line(date_start, date_finish, label):
    """
    counts values for different line graphs
    :param date_start: beginning
    :param date_finish: ending
    :param label: line label
    :returns: list of values for line, name of line, true if cause
    """
    dates = list(date_iterator(date_start, date_finish))
    timeline = {date: i for (i, date) in enumerate(dates)}
    cnts = [0 for _ in range(len(dates))]  # to ensure order
    res = [0 for _ in range(len(dates))]

    is_cause = False

    for fire_id in fire_data.keys():
        fire = fire_data[fire_id]

        # ensuring there are boundaries
        fires_start_day = fire["date_start"]
        if fires_start_day is None:
            fires_start_day = date_start
        else:
            fires_start_day = fires_start_day.date()
        fire_end_day = fire["date_finish"]
        if fire_end_day is None:
            fire_end_day = date_finish
        else:
            fire_end_day = fire_end_day.date()

        d1 = set(date_iterator(fires_start_day, fire_end_day))  # set of days when fire was there
        d2 = set(dates)  # considered time period

        is_mean = False  # should mean result be returned

        for day in d1 & d2:  # on intersection
            match label:
                case "Количество":
                    name = "количество пожаров"
                    res[timeline[day]] += 1

                case "Площадь":
                    name = "общая площадь возгорания"
                    if fire["area"] is not None:
                        res[timeline[day]] += fire["area"]

                case "Среднее время":
                    is_mean = True
                    name = "среднее время устранения"
                    if fire["date_finish"] is not None and fire["date_start"] is not None:
                        cnts[timeline[day]] += 1
                        res[timeline[day]] += (fire["date_finish"] - fire["date_start"]).days + 1

                case cause:  # for fire causes (each cause is a separate line)
                    name = cause
                    is_cause = True
                    if fire["cause"] == cause:
                        cnts[timeline[day]] += 1

    if (date_finish - date_start).days >= 21:
        weeks_number = date_finish.isocalendar().week - date_start.isocalendar().week + 1
        start_week = date_start.isocalendar().week

        weeks_res = [0 for _ in range(weeks_number)]
        weeks_cnts = [0 for _ in range(weeks_number)]

        for date in dates:
            week_id = date.isocalendar().week - start_week
            weeks_res[week_id] += res[timeline[date]]
            if is_mean:  # if counters required
                weeks_cnts[week_id] += cnts[timeline[date]]

        if is_mean:
            for i in range(len(weeks_res)):
                if weeks_cnts[i] != 0:
                    weeks_res[i] = weeks_res[i] / weeks_cnts[i]
                else:
                    weeks_res[i] = 0

        return weeks_res, name, is_cause

    if is_mean:
        for i in range(len(res)):
            if cnts[i] != 0:
                res[i] = res[i] / cnts[i]
            else:
                res[i] = 0

    return res, name, is_cause


def plot_lines(date_start, date_finish, lines, contains_causes):
    """
    plots all lines from list "lines"
    :param date_start: beginning
    :param date_finish: ending
    :param lines: list of points for lines
    :param contains_causes: special flag for graph of causes
    :returns: name of temporary file with plot
    """
    dates = list(date_iterator(date_start, date_finish))
    plt.grid()

    y_axis_cnt = 0  # to keep track of y-axes

    if (date_finish - date_start).days < 21:
        fig, ax = plt.subplots()
        x = [i.strftime("%d.%m") for i in dates]
        if (date_finish - date_start).days > 10:
            ax.set_xticks([i.strftime("%d.%m") for i in dates if i.day % 2 == dates[0].day % 2])

        if contains_causes:
            y_axis_cnt = 1  # reserving first y-axis for causes

        for line in lines:
            if line[2]:
                ax.plot(x, line[0], label=line[1])
            else:
                match y_axis_cnt:
                    case 0:
                        ax.plot(x, line[0], label=line[1])
                    case 1:
                        ax2 = ax.twinx()
                        ax2.plot(x, line[0], label=line[1], color="red")
                    case 2:
                        ax3 = ax.twinx()
                        ax3.plot(x, line[0], label=line[1], color="green")
                        ax3.spines['left'].set_position(('axes', 2))
                    case 4:
                        ax4 = ax.twinx()
                        ax4.plot(x, line[0], label=line[1], color="orange")
                        ax4.spines['right'].set_position(('axes', 2 ))
                y_axis_cnt += 1

        plt.xlabel("дата")
        plt.legend()
        fig.autofmt_xdate()

    else:
        week_num = date_finish.isocalendar().week - date_start.isocalendar().week + 1
        start_week = date_start.isocalendar().week

        fig, ax = plt.subplots()
        x = [f"нед. {start_week + i}" for i in range(week_num)]

        if len(x) > 20:
            ax.set_xticks([start_week + i for i in range(week_num) if i % 3 == 0])

        for line in lines:
            if line[2]:
                ax.plot(x, line[0], label=f"{line[1]}")
            else:
                match y_axis_cnt:
                    case 0:
                        ax.plot(x, line[0], label=f"{line[1]}")
                    case 1:
                        ax2 = ax.twinx()
                        ax2.plot(x, line[0], label=f"{line[1]}", color="red")
                    case 2:
                        ax3 = ax.twinx()
                        ax3.plot(x, line[0], label=f"{line[1]}", color="green")
                        ax3.spines['left'].set_position(('axes', 2))
                    case 4:
                        ax4 = ax.twinx()
                        ax4.plot(x, line[0], label=f"{line[1]}", color="orange")
                        ax4.spines['right'].set_position(('axes', 2))
                y_axis_cnt += 1
        plt.xlabel("номер недели в году")
        plt.legend()
        fig.autofmt_xdate()

    f_name = f"{randint(1, 10000)}.png"
    plt.savefig(f_name)

    return open(f_name, "rb")


# def plot_pie(date_start, date_finish, sections, number):


def build_linear_plot(sections, first_date, second_date):
    lines = []
    contains_causes = False
    for section in sections:
        if section == "Причины":
            contains_causes = True
            causes = set([fire_data[f]["cause"] for f in fire_data.keys()])
            for cause in causes:
                lines.append(get_line(first_date.date(), second_date.date(), cause))
        else:
            lines.append(get_line(first_date.date(), second_date.date(), section))
    return plot_lines(first_date, second_date, lines, contains_causes)


def build_pie_chart(sections, first_date, second_date):
    pass


if __name__ == "__main__":
    print(build_linear_plot({"Количество", "Причины", "Площадь"}, datetime(year=2022, month=2, day=1),
                            datetime(year=2022, month=12, day=20)))
