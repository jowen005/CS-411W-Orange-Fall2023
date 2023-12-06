from numpy import polyfit

DEGREE = 5


def calculate(analytics_set, trend_types):
    
    # print(analytics_set) #NOTE
    num_analytics = analytics_set.count()
    if num_analytics < 5:
        print(f'\tOnly {num_analytics} data points were found in the Analytics Table, while 5 are required.')
        return
    
    analytics_set = analytics_set.order_by('date_stamp')

    first_datestamp = analytics_set.first().date_stamp
    last_datestamp = analytics_set.last().date_stamp

    first_timestamp = analytics_set[0].date_stamp.timestamp()
    dates = [analytic.date_stamp.timestamp() - first_timestamp for analytic in analytics_set]
    # print(dates) #NOTE

    trend_data = []
    for trend_type, analytic_attr in trend_types:
        values = [float(val) for val in analytics_set.values_list(analytic_attr, flat=True)]
        coefficients = list(polyfit(dates, values, DEGREE))
        coefficients.reverse()
        # print(coefficients) #NOTE

        data = {'trend_type': trend_type}
        for idx, coeff in enumerate(coefficients):
            # print(f'{idx} - {coeff}') #NOTE
            data[f'coeff{idx}'] = coeff
        data['x_min'] = first_datestamp
        data['x_max'] = last_datestamp
        data['y_min'] = min(values)
        data['y_max'] = max(values)
        # print(data) #NOTE

        trend_data.append(data)

    return trend_data

