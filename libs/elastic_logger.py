import elasticsearch
import traceback
from configparser import RawConfigParser
from datetime import datetime
from logging import Handler, Formatter


class ElasticHandler(Handler):
    def __init__(self, config_file):
        Handler.__init__(self)

        config = RawConfigParser()
        config.read(config_file)
        es_host = config.get('gradiusbot', 'elastic_url')

        self.elastic = elasticsearch.Elasticsearch([es_host])
        self.index_name = config.get('gradiusbot', 'es_log_index')

    def emit(self, record):
        log_entry = self.format(record)
        index_name = self.index_name
        doc_type = 'python_log'
        try:
            self.elastic.index(index=index_name, doc_type=doc_type, body=log_entry)
        except:
            print(traceback.format_exc())


class ElasticFormatter(Formatter):
    def __init__(self):
        Formatter.__init__(self)

    def format(self, record):
        data = {
            '@timezone': datetime.utcnow(),
            'name': record.name,
            'level': record.levelname,
            'message': record.msg,
            'path': record.pathname,
            'line_num': record.lineno,
            'function': record.funcName
        }
        return data
