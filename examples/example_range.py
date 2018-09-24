import ecal


def main():

    print('Get the earnings announcements for a date range:')
    cal_df = ecal.get('2018-01-01', '2018-01-05')
    print(cal_df)


if __name__ == '__main__':
    main()
