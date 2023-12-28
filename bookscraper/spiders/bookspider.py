import scrapy
from bookscraper.items import BookItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        main_url = "https://books.toscrape.com/"
        
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            
            if 'catalogue/' in relative_url:
                book_link = main_url + relative_url
            else:
                book_link = main_url + 'catalogue/' + relative_url
            
            yield response.follow(book_link, callback = self.parse_book_page)
            
        next_page = response.css('li.next a ::attr(href)').get()
        
        if next_page is not None:
            
            if 'catalogue/' in next_page:
                next_page_url = main_url + next_page
            else:
                next_page_url = main_url + 'catalogue/' + next_page
                
            yield response.follow(next_page_url, callback = self.parse)
            
    def parse_book_page(self, response):        
        table_rows = response.css('tr')
        
        bookItem = BookItem()
        
        bookItem['Url'] = response.url
        bookItem['Title'] = response.css('div.product_main h1 ::text').get()
        bookItem['Description'] = response.selector.xpath('//*[@id="content_inner"]/article/p/text()').get()
        bookItem['Theme'] = response.selector.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        bookItem['Price'] = response.css('p.price_color ::text').get()
        bookItem['UPC'] =  table_rows[0].css('td ::text').get()
        bookItem['Product_Type'] =  table_rows[1].css('td ::text').get()
        bookItem['Price_excl_tax'] =  table_rows[2].css('td ::text').get()
        bookItem['Price_incl_tax'] =  table_rows[3].css('td ::text').get()
        bookItem['Tax'] =  table_rows[4].css('td ::text').get()
        bookItem['Availability'] =  table_rows[5].css('td ::text').get()
        bookItem['Number_of_reviews'] =  table_rows[6].css('td ::text').get()

        yield bookItem