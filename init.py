if __name__ == '__main__':
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    curve = []
    years = ["2023", "2024"]

    for y in years:
        for m in range(len(MONTHS)):
            this_month = MONTHS[m]
            next_month = MONTHS[m]
            if m < len(MONTHS) - 1:
                next_month = MONTHS[m + 1]
            else:
                next_month = MONTHS[0]
            curve.append(this_month + y[2:]+ "/" + next_month + y[2:])
