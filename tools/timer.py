# coding:utf-8


from time import time, sleep


def get_hours_minutes_seconds(seconds):
	hours	= seconds // 3600
	minutes	= seconds // 60 % 60
	seconds	= seconds % 60
	return hours, minutes, seconds


def get_time_or_not_for_method(get=True):
    def timer(method):
        def wrapper(self, *arg, **kwargs):
            if get == True:
                start_time = time()
                method(self, *arg, **kwargs)
                end_time = time()

                total_time = end_time - start_time

                print('耗时：', end='')
                if total_time < 60:
                    print('%.2f 秒' % total_time)
                elif 60 <= total_time <= 3559:
                    total_time /= 60
                    print('%.2f 分钟' % total_time)
                elif 3600 <= total_time:
                    total_time /= 3600
                    print('%.2f 小时' % total_time)
                print('\n')
            else:
                method(self, *arg, **kwargs)

        return wrapper

    return timer


def get_time_or_not_for_function(get=True):
    def timer(func):
        def wrapper(*arg, **kwargs):
            if get == True:
                start_time = time()
                func(*arg, **kwargs)
                end_time = time()

                total_time = end_time - start_time

                if total_time <= 60:
                    print('耗时:%.2f 秒' % total_time)
                else:
                    total_time /= 60
                    print('耗时:%.2f 分钟' % total_time)
            else:
                func(*arg, **kwargs)

        return wrapper

    return timer


class C:
    @get_time_or_not_for_method(get=True)
    def mysleep(self, arg):
        sleep(arg)


@get_time_or_not_for_function()
def a_sleep(args):
    sleep(args)


if __name__ == '__main__':
    c = C()
    c.mysleep(0.01)

    a_sleep(0.02)

    f = get_hours_minutes_seconds
    assert f(1) == (0, 0, 1)
    assert f(17) == (0, 0, 17)
    assert f(59) == (0, 0, 59)
    assert f(60) == (0, 1, 0)
    assert f(61) == (0, 1, 1)
    assert f(67) == (0, 1, 7)
    assert f(119) == (0, 1, 59)
    assert f(120) == (0, 2, 0)
    assert f(121) == (0, 2, 1)
    assert f(132) == (0, 2, 12)
    assert f(3599) == (0, 59, 59)
    assert f(3600) == (1, 0, 0)
    assert f(3601) == (1, 0, 1)
    assert f(3763) == (1, 2, 43)
    print('Pass!')
