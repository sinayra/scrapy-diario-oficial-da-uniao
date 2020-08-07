import json
import logging
from itemadapter import ItemAdapter
from queue import Queue

# pipeline to fill the items list
class ItemCollectorPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name + '.jl', 'w', encoding='utf-8')
        self.logger = logging.getLogger(__name__)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)

        if spider.name == "secoes-diario-oficial-da-uniao":
            spider.consumer_queue.put(spider.itemScrapped * -1)
        return item