# coding:utf-8

from py2neo import Graph, Node, Relationship
from tools.make_a_list_of_strings import make_a_list_of_strings
from tools.files import *
from tools.timer import get_time_or_not_for_method
from tools.transfer_chinese_words_to_pinyins import transfer_chinese_words_to_pinyins

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

        self.g = None
        self.transaction = None

    def connect_data_base(self, scheme='http', host='0.0.0.0', port=7474, \
                          username='neo4j', password='heli111111'):
        self.g = Graph(scheme=scheme, host=host, username=username, password=password)
        self.transaction = self.g.begin()

    #@get_time_or_not_for_method(get=False)
    def batch_load(self, source_file, mapper_file, n=3):
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

        for line in open(source_file):
            if line == '\n':
                break

            entity_name, property_name, property_value = make_a_list_of_strings(line)
            #property_name = get_pinyin_n(property_name)

            if entity_name not in self.entity_name_cache:
                if len(self.node_queue) == n:
                    commit_no_more_than_n_nodes_per_trans(n)

                self.node = Node()
                set_entity_name_of_node()

            set_property_of_node()

        commit_no_more_than_n_nodes_per_trans(n)


if __name__ == '__main__':
    source_file = total_txt_9_lines
    mapper_file = total_txt_9_lines_mapper_of_property_names_to_pinyins

    dm = DataModel()
    dm.batch_load(source_file, mapper_file)
