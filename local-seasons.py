import numpy as np
from scipy.interpolate import interp1d
import datetime

# Data from Barcelona, Can Bruixa
# Extracted from Wikipedia
monthly_temp_dict = {}

monthly_temp_dict['Barcelona'] = [11.7, 12.4, 14.2, 15.8, 19.3, 23.0, 25.7, 26.1, 23.0, 19.5, 14.9, 12.3]

# madrid, parque del retiro
monthly_temp_dict['Madrid'] = [6.45, 7.72, 11.0, 13.65, 17.22, 23.15, 25.78, 25.31, 21.03, 15.38, 9.50, 6.47]

days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
accum_days_month = [sum(days_per_month[0:i]) + days_per_month[i]/2 - 1 
                    for i in range(12)]
days = range(365)
# extrend dates to previous and next year
accum_days_month = ([x - 365 for x in accum_days_month] 
                    + accum_days_month 
                    + [x + 365 for x in accum_days_month])

for location in monthly_temp_dict:

    monthly_temp = monthly_temp_dict[location]
    
    monthly_temp = 3*monthly_temp # past and next years also

    interp_temp = interp1d(accum_days_month, monthly_temp, 'cubic')
    daily_temp = interp_temp(days)

    sorted_temps = sorted(zip(daily_temp, days))

    coolest_temp, coolest_day = min(sorted_temps)
    warmest_temp, warmest_day = max(sorted_temps)

    temp_diff = warmest_temp - coolest_temp

    def to_date(day):
        date_0 = datetime.datetime.strptime("01/01/17", "%d/%m/%y") # arbitrary non-leap year
        date = date_0 + datetime.timedelta(days=day)
        return date.strftime("%d %B")

    print('LOCATION: {}'.format(location))
    print("Coolest day: {} ({:.1f} ºC)".format(to_date(coolest_day), coolest_temp))
    print("Warmest day: {} ({:.1f} ºC)".format(to_date(warmest_day), warmest_temp))

    print("")
    print("Seasons - method 1")
    winter_days_beg = [days for _, days in sorted_temps[1:90] if days < 365/2]
    winter_days_end = [days for _, days in sorted_temps[1:90] if days > 365/2]
    winter_start = min(winter_days_end)
    winter_end = max(winter_days_beg)
    summer_days = [days for _, days in sorted_temps[-92:-1]]
    summer_start = min(summer_days)
    summer_end = max(summer_days)
    print("Spring: {} - {}".format(to_date(winter_end+1), to_date(summer_start-1)))
    print("Summer: {} - {}".format(to_date(summer_start), to_date(summer_end)))
    print("Autumn: {} - {}".format(to_date(summer_end+1), to_date(winter_start-1)))
    print("Winter: {} - {}".format(to_date(winter_start), to_date(winter_end)))

    print("")
    print("Seasons - method 2")
    temp_th1 = coolest_temp + temp_diff/4
    temp_th2 = coolest_temp + temp_diff*3/4
    winter_days_2_beg = [days for temp, days in sorted_temps if days < 365/2 and temp < temp_th1]
    winter_days_2_end = [days for temp, days in sorted_temps if days > 365/2 and temp < temp_th1]
    winter_2_start = min(winter_days_2_end)
    winter_2_end = max(winter_days_2_beg)
    summer_2_days = [days for temp, days in sorted_temps if temp > temp_th2]
    summer_2_start = min(summer_2_days)
    summer_2_end = max(summer_2_days)
    print("Spring: {} - {}".format(to_date(winter_2_end+1), to_date(summer_2_start-1)))
    print("Summer: {} - {}".format(to_date(summer_2_start), to_date(summer_2_end)))
    print("Autumn: {} - {}".format(to_date(summer_2_end+1), to_date(winter_2_start-1)))
    print("Winter: {} - {}".format(to_date(winter_2_start), to_date(winter_2_end)))
    print("")



