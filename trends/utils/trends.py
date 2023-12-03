from numpy import polyfit

DEGREE = 5


def calculate(analytics_set, trend_types):
    
    # print(f'{AnalyticsModel.__name__}:')
    num_analytics = analytics_set.count()
    if num_analytics < 5:
        print(f'\tOnly {num_analytics} data points were found in the Analytics Table, while 5 are required.')
        return
    
    analytics_set = analytics_set.order_by('date_stamp')
    first_timestamp = analytics_set[0].date_stamp.timestamp()
    dates = [analytic.date_stamp.timestamp() - first_timestamp for analytic in analytics_set]

    trend_data = []
    for trend_type, analytic_attr in trend_types:
        values = list(analytics_set.values_list(analytic_attr, flat=True))
        coefficients = list(polyfit(dates, values, DEGREE)).reverse()

        data = {'trend_type': trend_type}
        for idx, coeff in enumerate(coefficients):
            data[f'coeff{idx}'] = coeff
        data['behavior'] = '' #TODO

        trend_data.append(data)

    return trend_data

