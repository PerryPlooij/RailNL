def calculate_quality(connections, connection_total, trajects):
    """ Calculate quality of the created train lining system based on the fraction connections used, the amount of
        trajects and the total time of the trian lining system.
    """

    minutes = 0
    p = 1 - connections / connection_total
    T = len(trajects)

    for key, value in trajects.items():
        minutes += value[1]

    K = p * 10000 - (T * 100 + minutes)
    return K