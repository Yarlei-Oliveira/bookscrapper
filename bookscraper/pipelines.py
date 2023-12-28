# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        
        ## Price
        
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
        
        price_keys = ['Price', 'Tax', 'Price_excl_tax', 'Price_incl_tax']
        
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)
        
        ## Availability
        
        availability_key = 'Availability'
        value = adapter.get(availability_key)
        value = value.replace('In stock (', '')
        value = value.replace(')', '')
        
        adapter[availability_key] = value
        
        ## Number of reviews
        
        review_key = 'Number_of_reviews'
        
        value = adapter.get(review_key)
        value = int(value)
        adapter[review_key] = value
        
        return item
