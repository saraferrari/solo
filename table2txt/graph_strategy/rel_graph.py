import random
import numpy as np
from table2txt.graph_strategy.strategy import Strategy 
from table2txt.graph_strategy.rel_tags import RelationTag

class RelationGraph(Strategy):
    def __init__(self):
        super(RelationGraph, self).__init__()

    def get_topic_entity(self, table):
        topic_entity = table['documentTitle'].strip()
        return topic_entity
    
    def update_cells(self, table):
        col_data = table['columns']
        row_data = table['rows']

        for col_idx, col_info in enumerate(col_data):
            col_info['text'] = col_info['text'].strip()

        for row_info in row_data:
            cell_data = row_info['cells'] 
            for cell_info in cell_data:
                cell_info['text'] = cell_info['text'].strip()

    def gen_topic_entity_rels(self, table):
        topic_entity = self.get_topic_entity(table)
        if topic_entity != '':
            col_data = table['columns']
            row_data = table['rows']
            for row_idx, row_info in enumerate(row_data):
                for col_idx, col_info in enumerate(col_data):
                    rel_name = col_info['text']
                    obj = row_info['cells'][col_idx]['text'] 
                    graph = RelationTag.get_annotated_text(topic_entity, None, None, rel_name, obj) 
                    graph_info = {
                        'table_id':table['tableId'],
                        'row':row_idx,
                        'sub_col':None,
                        'obj_col':col_idx,
                        'graph':graph
                    }
                    yield graph_info

    def gen_row_rels(self, table):
        topic_entity = self.get_topic_entity(table)
        col_data = table['columns']
        N = len(col_data)
        row_data = table['rows']
        for row_idx, row_info in enumerate(row_data):
            for sub_col_idx in range(N-1):
                sub_name = col_data[sub_col_idx]['text']
                sub = row_info['cells'][sub_col_idx]['text']
                for obj_col_idx in range(sub_col_idx+1, N):
                    rel_name = col_data[obj_col_idx]['text']
                    obj = row_info['cells'][obj_col_idx]['text']
                    graph = RelationTag.get_annotated_text(topic_entity, sub_name, sub, rel_name, obj) 
                    graph_info = {
                        'table_id':table['tableId'],
                        'row':row_idx,
                        'sub_col':sub_col_idx,
                        'obj_col':obj_col_idx,
                        'graph':graph
                    }
                    yield graph_info 

    def generate(self, table):
        self.update_cells(table)
       
        triple_dict = {} 
        for graph_info_topic in self.gen_topic_entity_rels(table):
            graph_key = graph_info_topic['graph'].strip().lower()
            if graph_key not in triple_dict:
                triple_dict[graph_key] = True
                yield graph_info_topic
        
        for graph_info_row in self.gen_row_rels(table):
            graph_key_row = graph_info_row['graph'].strip().lower()
            if graph_key_row not in triple_dict:
                triple_dict[graph_key_row] = True
                yield graph_info_row

