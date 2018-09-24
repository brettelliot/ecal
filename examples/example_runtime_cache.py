import ecal
import time


def main():

    print('Geting the earnings announcements for a date range and cache it.')
    print('This first call will take ~ 8 seconds...')
    pre_call_time = time.time()
    cal_df = ecal.get('2018-01-01', '2018-01-05')
    print('The first call to ecal.get took {} seconds'.format(time.time() - pre_call_time))
    print(cal_df)

    print('By default, ecal uses an instance of RuntimeCache.')
    print('The second time, ecal.get will use the cache.')
    pre_call_time = time.time()
    cal_df = ecal.get('2018-01-01', '2018-01-05')
    print('The second call to ecal.get took {} seconds'.format(time.time() - pre_call_time))
    print(cal_df)

    print('The third call, ecal.get will use the cache. This one asks for dates with no announcements:')
    pre_call_time = time.time()
    cal_df = ecal.get('2018-01-01', '2018-01-02')
    print('The third call to ecal.get took {} seconds'.format(time.time() - pre_call_time))
    print(cal_df)


if __name__ == '__main__':
    main()
