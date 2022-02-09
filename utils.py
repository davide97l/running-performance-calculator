import streamlit as st
import math


def get_pace(dist, time, mile=False):
    if not mile:
        pace = (time/dist)/60.*1000.
    else:
        pace = (time/dist)/60.*1609.32
    pace_min = math.floor(pace)
    pace_sec = round((pace % 1) * 60)
    if (pace % 1) * 60 > 59.5:
        pace_min += 1
        pace_sec = 0
    return pace_min, pace_sec


def c_to_f(temp):
    return temp * 9/5 + 32


def f_to_c(temp):
    return (temp - 32) * 5/9


def pace_temperature(time, temp, temp_t):
    # http://maximumperformancerunning.blogspot.com/2013/05/training-in-summer-heathumidity.html
    """dist (m), time (sec), temp (C)"""
    heat_threshold = 60
    temp, temp_t = c_to_f(temp), c_to_f(temp_t)
    if temp < heat_threshold:
        temp = heat_threshold
    if temp_t < heat_threshold:
        temp_t = heat_threshold
    diff_temp = temp_t - temp
    return time * 0.01 * diff_temp


def incline(dist, elev):
    return elev / dist * 100


def pace_elevation(dist, time, elev):
    # https://www.runnersworld.com/advanced/a20820206/downhill-all-the-way/
    """dist (m), time (sec), temp (C)"""
    slope = incline(dist, elev)
    if slope >= 0:
        c = 0.033
    else:
        c = 0.018
    delta_elev = slope * c * time
    return delta_elev


def pace_altitude(time, alt):
    c = 304.8  # 1000 feet
    delta_alt = time * alt / c * 0.01
    return delta_alt


def sec_to_time(sec):
    h = int(sec / 3600)
    m = int(sec % 3600 / 60)
    s = int(sec % 3600 % 60)
    return h, m, s


DIST = {
    "Mile": 1609.34,
    "5km": 5000.,
    "10km": 10000.,
    "Halfmarathon": 21097.,
    "Marathon": 42195.,
    "Custom": None,
}


def diff_time_str(sec1, sec2, has_h=True):
    diff = sec1 - sec2
    ret = time_str(diff, has_h=has_h)
    if sec1 > sec2:
        ret = str('-') + ret
    return ret


def time_str(sec, has_h=True):
    h, m, s = sec_to_time(abs(sec))
    if h == 0 and m == 0:
        ret = str(s) + 's'
    elif h == 0 and m != 0:
        ret = str(m) + 'm' + str(s) + 's'
    else:
        if has_h:
            ret = str(h) + 'h' + str(m) + 'm' + str(s) + 's'
        else:
            ret = str(m + h * 60) + 'm' + str(s) + 's'
    return ret


def format_time(h, m, s):
    hms = [h, m, s]
    try:
        #for i in range(3):
        #if len(hms[i]) == 0:
        #    return "Time entries can't be empty !"
        #hms[i] = hms[i].lstrip('0')
        #if len(hms[i]) == 0:
        #    hms[i] = '0'
        #hms[i] = int(hms[i])
        h, m, s = hms[0], hms[1], hms[2]
        if h < 0 or m < 0 or s < 0:
            return "Hours, minutes, and seconds should be >= 0. You can't travel back in time !"
        if s > 59 or m > 59:
            return "Minutes, and seconds can't exceed 59 !"
        if h == 0 and m == 0 and s == 0:
            return "You can't use instant teleport !"
        return h, m, s
    except:
        return 'Time not in the right format !'


def show():

    st.write("👉 Have you ever wondered if you ran 10km at 2000m altitude, how fast would you run the same distance at"
             " lower altitudes? How would elevation gain and temperature affect your performance? 🤔")
    st.write("👉 The goal of this application is to calculate how your running pace and time would change given different **elevation gain**,"
             " **altitude**, and **temperature**.")
    st.write("👉 Feel free to report any bug or suggestion on [Github](https://github.com/davide97l/running-performance-calculator) and leave a ⭐ if you found it useful.")

    st.write("## Distance 🛣️")
    default_distance = st.selectbox("Select distance", list(DIST.keys()))
    distance = DIST[default_distance]
    if distance is None:
        column1, column2 = st.columns(2)
        raw_distance = column1.number_input("Write your distance here", 1.0, 10000., 100.)
        distance = raw_distance
        dist_unit = column2.radio(
            "Unit",
            ('Meters (m)', 'Kilometers (km)', 'Miles (mi)'))
        if dist_unit == 'Kilometers (km)':
            distance *= 1000.
        elif dist_unit == 'Miles (mi)':
            distance *= 1609.34

    st.write("## Time ⏱️")
    if DIST[default_distance]:
        dist_name = default_distance
    else:
        if raw_distance.is_integer():
            raw_distance = int(raw_distance)
        dist_unit = dist_unit.split(' ')[0]
        if raw_distance == 1.:
            dist_unit = dist_unit[:-1]
        dist_name = str(raw_distance) + " " + str(dist_unit)
    text = "How long did it take to finish your {}?".format(dist_name)
    st.write(text)
    column1, column2, column3 = st.columns(3)
    h = column1.number_input("Hours", 0, 9999, 0)
    m = column2.number_input("Minutes", 0, 59, 30)
    s = column3.number_input("Seconds", 0, 59, 0)
    time = format_time(h, m, s)
    if type(time) == str:
        st.error(time)
    else:
        h, m, s = time
        time = h * 3600 + m * 60 + s
        pace, pace_mile = get_pace(distance, time, mile=False), get_pace(distance, time, mile=True)
        st.write("Average pace: {}m{}s/km or {}m{}s/mile".format(pace[0], pace[1], pace_mile[0], pace_mile[1]))

        st.write("## Real Environment ⛰️")
        column1, column2 = st.columns(2)
        elev = column1.number_input("Write the elevation gain here (m)", -100000, 100000, 0)
        column1.write("Average inclination: {:.2f}%".format(incline(distance, elev)))
        alt = column2.number_input("Write the altitude here (m)", -10000, 10000, 0)
        column1, column2 = st.columns(2)
        temp = column1.number_input("Write the temperature here", -50, 50, 16)
        temp_unit = column2.radio(
            "Unit",
            ('Celsius (°C)', 'Fahrenheit (°F)'))
        if temp_unit == 'Fahrenheit (°F)':
            temp = f_to_c(temp)
            temp_unit_str = "°F"
        else:
            temp_unit_str = "°C"

        st.write("## Target Environment 🎯")
        column1, column2 = st.columns(2)
        elev_t = column1.number_input("Write the elevation gain here (m)", -100000, 100000, 0, key='target')
        column1.write("Average inclination: {:.2f}%".format(incline(distance, elev_t)))
        alt_t = column2.number_input("Write the altitude here (m)", 0, 10000, 0, key='target')
        column1, column2 = st.columns(2)
        temp_t = column1.number_input("Write the temperature here", -100, 100, 16, key='target')
        temp_unit_t = column2.radio(
            "Unit",
            ('Celsius (°C)', 'Fahrenheit (°F)'), key='target')
        if temp_unit_t == 'Fahrenheit (°F)':
            temp_t = f_to_c(temp_t)
            temp_unit_str_t = "°F"
        else:
            temp_unit_str_t = "°C"

        st.write("## Report 📈")

        delta_temp = pace_temperature(time, temp, temp_t)
        delta_alt = pace_altitude(time, alt_t-alt)
        delta_elev = pace_elevation(distance, time, elev_t-elev)

        col1, col2, col3 = st.columns(3)

        if temp_unit_t == "°F":
            temp, temp_t = c_to_f(temp), c_to_f(temp_t)
        col1.metric("Temperature", "{} {}".format(temp_t, temp_unit_str_t), "{} {}".format(temp_t-temp, temp_unit_str_t))
        col2.metric("Elevation Gain", "{}m".format(elev_t), "{}m".format(elev_t-elev))
        col3.metric("Altitude", "{}m".format(alt_t), "{}m".format(alt_t-alt))

        time_t = time + delta_temp + delta_alt + delta_elev
        #h, m, s = sec_to_time(time)
        #h_t, m_t, s_t = sec_to_time(time_t)
        pace_t = get_pace(distance, time_t, mile=False)
        pace_mile_t = get_pace(distance, time_t, mile=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Time", time_str(time_t), diff_time_str(time, time_t), delta_color='inverse')
        col2.metric("Pace (min/km)", "{}m{}s".format(pace_t[0], pace_t[1]),
                    diff_time_str(pace[0]*60 + pace[1], pace_t[0] * 60 + pace_t[1], has_h=False), delta_color='inverse')
        col3.metric("Pace (mile/km)", "{}m{}s".format(pace_mile_t[0], pace_mile_t[1]),
                    diff_time_str(pace_mile[0]*60 + pace_mile[1], pace_mile_t[0] * 60 + pace_mile_t[1], has_h=False),
                    delta_color='inverse')

        st.write("## Note ✔️")

        st.info("The above data is an estimation of your hypothetical performance. Real stats may vary according to your"
                " degree of acclimatization to the target environment and your overall fitness.")


if __name__ == "__main__":
    show()


"""
streamlit run app/main.py

heroku create
git push heroku main
heroku open
"""
