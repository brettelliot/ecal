import ecal


def main():

    print('Get the earnings announcements for a single date:')
    cal_df = ecal.get('2017-03-30')
    print(cal_df)


if __name__ == '__main__':
    main()
