# coding:utf-8

from py2neo import Graph, Node, Relationship
from tools.make_a_list_of_strings import make_a_list_of_strings
from tools.files import *
from tools.timer import get_time_or_not_for_method, get_hours_minutes_seconds
from tools.transfer_chinese_words_to_pinyins import transfer_chinese_words_to_pinyins
import sys
from time import time


'''
class DomainModel(DataModel):
    def __init__(self):
        pass

    def query(self):
        pass

    def remove(self):
        pass

    def append(self, entity_name, property_name, property_value):
        pass
'''


class DataModel(object):
    def __init__(self):
        self.entity_name_cache = set()
        self.property_name_cache = set()
        self.node_queue = list()
        self.node = None
        self.line_count = 0

        self.g = None
        self.transaction = None

    def connect_data_base(self, scheme='http', host='0.0.0.0', port=7474, \
                          username='neo4j', password='heli111111'):
        self.g = Graph(scheme=scheme, host=host, port=port, username=username, password=password)
        self.transaction = self.g.begin()

    @get_time_or_not_for_method(get=True)
    def batch_load(self, source_file, mapper_file, n, want_progress=True):
        def get_pinyin_n(property_name):
            for line in open(mapper_file):
                hanzis, pinyins = make_a_list_of_strings(line, sep=' ')
                if property_name == hanzis:
                    return pinyins

        def set_property_of_node():
            if property_name not in self.property_name_cache:
                self.property_name_cache = set()
                self.property_name_cache.add(property_name)

            if self.node[property_name] is None:
                self.node[property_name] = [property_value]
            else:
                self.node[property_name].append(property_value)

        def set_entity_name_of_node():
            self.node_queue.append(self.node)

            self.entity_name_cache = set()
            self.entity_name_cache.add(entity_name)

            self.node['entity_name'] = entity_name

        def commit_head_node():
            head_node = self.node_queue.pop(0)
            self.connect_data_base()
            self.transaction.create(head_node)
            self.transaction.commit()

        def commit_no_more_than_n_nodes_per_trans(n):
            self.connect_data_base()

            for _ in range(n):
                if len(self.node_queue) >= 1:
                    head_node = self.node_queue.pop(0)
                    self.transaction.create(head_node)
                else:
                    break

            self.transaction.commit()

        def get_number_of_lines_of_txt_files(file_name):
            d = {
                total_txt_9_lines:      10,
                total_txt_49_lines:     39,
                total_txt_1_to_10000:   6499,
                total_txt_1_to_1000:    65000,
                total_txt_1_to_10:      6500129,
                total_txt:              65001290
            }
            return d[file_name]

        def show_progress():

            self.line_count += 1

            percent = self.line_count / total_number_of_lines
            percent100 = percent * 100

            end_time = time()

            seconds = end_time - start_time

            hours, minutes, seconds = get_hours_minutes_seconds(seconds)

            need_seconds = seconds * (1 - percent) / percent

            need_hours, need_minutes, need_seconds = get_hours_minutes_seconds(need_seconds)
            sys.stdout.write("\r已处理约 %.3f%% 的数据，"
                             "已累计耗时 %d 小时 %d 分钟 %d 秒，预计还需要 %d 小时 %d 分钟 %d 秒..."
                             % (percent100, hours, minutes, seconds, need_hours, need_minutes, need_seconds))

        total_number_of_lines = get_number_of_lines_of_txt_files(source_file)

        print('\n')

        start_time = time()

        for line in open(source_file):
            if line == '\n':
                break

            entity_name, property_name, property_value = make_a_list_of_strings(line)

            if entity_name not in self.entity_name_cache:
                if len(self.node_queue) == n:
                    commit_no_more_than_n_nodes_per_trans(n)

                self.node = Node()
                set_entity_name_of_node()

            if property_name == 'BaiduTAG':
                self.node.add_label(property_value)
            else:
                # property_name = get_pinyin_n(property_name)
                set_property_of_node()

            if want_progress == True:
                show_progress()

        sys.stdout.write('\n\n就快处理完了...')

        commit_no_more_than_n_nodes_per_trans(n)

        sys.stdout.write('\n\n数据已经完全导入数据库！\n\n')


if __name__ == '__main__':
    source_file = total_txt_1_to_10000
    mapper_file = total_txt_9_lines_mapper_of_property_names_to_pinyins
    n = 100

    dm = DataModel()
    dm.batch_load(source_file, mapper_file, n)
