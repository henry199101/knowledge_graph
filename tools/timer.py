# coding:utf-8


from time import time, sleep


def get_time_or_not_for_method(get=True):
    def timer(method):
        def wrapper(self, *arg, **kwargs):
            if get == True:
                start_time = time()
                method(self, *arg, **kwargs)
                end_time = time()

                total_time = end_time - start_time

                if total_time <= 60:
                    print('耗时:%.2f 秒' % total_time)
                else:
                    total_time /= 60
                    print('耗时:%.2f 分钟' % total_time)
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
