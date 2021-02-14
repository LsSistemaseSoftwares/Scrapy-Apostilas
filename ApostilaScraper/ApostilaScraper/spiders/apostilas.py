import scrapy
from scrapy.loader import ItemLoader
from ApostilaScraper.items import ApostilaItems, ProgramaSemanaItems

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
            yield scrapy.Request(url, self.parse_apostila_hrefs, cb_kwargs={'items_pai': loader.load_item()})
            

    def parse_apostila_hrefs(self, response, items_pai):

        urls = response.css('div.syn-body.textOnly.accordionHandle > h2 > a::attr(href)').getall()
        for url in urls:
            yield response.follow(url, self.parse_designacoes_apostila, cb_kwargs={'items_pai':items_pai})

    def parse_designacoes_apostila(self, response, items_pai):
        
        loader = ItemLoader(item=ProgramaSemanaItems(), selector=response)
        loader.add_css('semana_referencia' , '#p1')
        loader.add_css('leitura_semana', '#p2')
        loader.add_css('cantico_inicial', '#p3')


        
        loader.add_css('tpd_titulo', '#section2 > div > ul > li:nth-child(1) > p')
        loader.add_css('tpd_href', '#section2 > div > ul > li:nth-child(1) > p > a::attr(href)')
        loader.add_css('tpd_duracao', '#section2 > div > ul > li:nth-child(1) > p')

        loader.add_css('tpd_joias_titulo', '#section2 > div > ul > li:nth-child(2) > p')
        loader.add_css('tpd_joias_duracao', '#section2 > div > ul > li:nth-child(2) > p')
        loader.add_css('tpd_joias_descricao', '#section2 > div.pGroup > ul > li:nth-child(2) > ul')

        loader.add_css('tpd_leitura_titulo', '#section2 > div.pGroup > ul > li:nth-child(3)')
        loader.add_css('tpd_leitura_duracao', '#section2 > div.pGroup > ul > li:nth-child(3)')
        loader.add_css('tpd_leitura_texto_base', '#section2 > div.pGroup > ul > li:nth-child(3) > p > a')
        loader.add_css('tpd_leitura_href', '#section2 > div.pGroup > ul > li:nth-child(3) > p > a::attr(href)')
        loader.add_css('tpd_leitura_licao_melhore_titulo', '#section2 > div.pGroup > ul > li:nth-child(3) > p > a.pub-th')
        loader.add_css('tpd_leitura_licao_melhore_href', '#section2 > div.pGroup > ul > li:nth-child(3) > p > a.pub-th::attr(href)')

        yield {
            "programa": items_pai,
            "designacoes": loader.load_item()
        }