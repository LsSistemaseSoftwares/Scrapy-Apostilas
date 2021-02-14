import scrapy
from scrapy.loader import ItemLoader
from ApostilaScraper.items import ApostilaItems

class ApostilaSpider(scrapy.Spider):
    name = 'apostila'
    start_urls = ['https://www.jw.org/pt/biblioteca/jw-apostila-do-mes/']

    def parse(self, response):
        
        apostilas = response.css('div.publicationDesc')[:8]
        for apostila in apostilas:

            loader = ItemLoader(item=ApostilaItems(), selector=apostila)
            loader.add_css('href', 'a::attr(href)')
            loader.add_css('descricao', 'a::text')
            loader.add_css('mes_inicio', 'a')
            loader.add_css('mes_fim', 'a')
            loader.add_css('ano_inicio', 'a')
            loader.add_css('ano_fim', 'a')

            url = f"https://www.jw.org{apostila.css('a::attr(href)').get()}"
            yield scrapy.Request(url, self.parse_programas_semana_details, cb_kwargs={'items_pai': loader.load_item()})
            

    def parse_programas_semana_details(self, response, items_pai):

        programas = response.css('div.syn-body.textOnly.accordionHandle::atrib(href)')
        yield programas

