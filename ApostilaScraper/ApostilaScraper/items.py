import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from ApostilaScraper.default import MesStrToInt


def remover_quebra_linhas(texto: str) -> str:
    return texto.replace('\n', '').strip()

def definir_mes_inicio(desc: str) -> int:
    
    Mes = MesStrToInt.__dict__
    try:
        # Janeiro–fevereiro de 2021
        mes_inicio = desc.split('–')[0].upper()
        return Mes[mes_inicio]
    except KeyError:
        #Dezembro de 2020
        mes_inicio = desc.replace('\xa0', ' ').split(' ')[0].upper()
        return Mes[mes_inicio]

def definir_mes_fim(desc: str) -> int:
    
    # Janeiro–fevereiro de 2021
    Mes = MesStrToInt.__dict__
    try:
        mes_fim = desc.split('–')[1].split(' ')[0].upper()
    except IndexError:
        #Dezembro de 2020
        mes_fim = desc.replace('\xa0', ' ').split(' ')[0].upper()
        
    return Mes[mes_fim]

def definir_ano_inicio_e_fim(desc: str) -> int:
    
    try:
        # Janeiro–fevereiro de 2021
        anoStr = desc.split(' ')[-1]
        return int(anoStr)
    except ValueError:
        #Dezembro de 2020
        anoStr = desc.replace('\xa0', ' ').split(' ')[-1]
        return int(anoStr)

def add_jw_prefix_to_href(href:str) -> str:
    return f'jw.org{href}'

class ApostilaItems(scrapy.Item):
    

    href = scrapy.Field(input_processor= MapCompose(add_jw_prefix_to_href), output_processor=TakeFirst())
    descricao = scrapy.Field(input_processor= MapCompose(remover_quebra_linhas), output_processor= TakeFirst())
    mes_inicio = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_mes_inicio), output_processor= TakeFirst())
    mes_fim = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_mes_fim), output_processor= TakeFirst())
    ano_inicio = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_ano_inicio_e_fim), output_processor= TakeFirst())
    ano_fim = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_ano_inicio_e_fim), output_processor= TakeFirst())
    programas_semana = scrapy.Field()

def get_titulo_de_descricao_com_duracao(desc: str) -> str:
    # Joias espirituais: (10 min)
    return desc.split(':')[0].replace('“', '').upper()

def get_duracao_de_descricao_com_duracao(desc: str) -> str:
    # Joias espirituais: (10 min)
    sem_paranteses = desc.replace('(', '').replace(')', '')
    return sem_paranteses.split(': ')[1].upper()

def get_duracao_de_descricao_com_duracao_mais_texto_base(desc:str) -> str:
    # Leitura da Bíblia: (4 min ou menos) Núm. 28:11-31 (Melhore lição 5)
    sem_paranteses = desc.split(')')[0].split('(')[1]
    return sem_paranteses

def get_lista_filha_as_string(lista_filha: str) -> str:
    
    items = lista_filha.replace('\xa0', '').replace('\r\r', '\n')
    return items

class ProgramaSemanaItems(scrapy.Item):

    semana_referencia = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas), output_processor= TakeFirst())
    leitura_semana = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas), output_processor= TakeFirst())
    cantico_inicial = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas), output_processor= TakeFirst())
    
    #Tesouros da Palavra de Deus
    tpd_titulo = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_titulo_de_descricao_com_duracao), output_processor= TakeFirst())
    tpd_href = scrapy.Field(input_processor= MapCompose(remove_tags, add_jw_prefix_to_href), output_processor= TakeFirst())
    tpd_duracao = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_duracao_de_descricao_com_duracao), output_processor= TakeFirst())

    tpd_joias_titulo = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_titulo_de_descricao_com_duracao), output_processor= TakeFirst())
    tpd_joias_duracao = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_duracao_de_descricao_com_duracao), output_processor= TakeFirst())
    tpd_joias_descricao = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_lista_filha_as_string), output_processor= TakeFirst())

    tpd_leitura_duracao = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_duracao_de_descricao_com_duracao_mais_texto_base), output_processor= TakeFirst())
    tpd_leitura_titulo = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_titulo_de_descricao_com_duracao), output_processor= TakeFirst())
    tpd_leitura_texto_base = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas), output_processor= TakeFirst())
    tpd_leitura_href = scrapy.Field(input_processor= MapCompose(remove_tags, add_jw_prefix_to_href), output_processor= TakeFirst())
    tpd_leitura_licao_melhore_titulo = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, get_titulo_de_descricao_com_duracao), output_processor= TakeFirst())
    tpd_leitura_licao_melhore_href = scrapy.Field(input_processor= MapCompose(remove_tags, add_jw_prefix_to_href), output_processor= TakeFirst())

    #Faça seu melhor no ministério
    fmm_design_1_titulo = scrapy.Field()
    fmm_design_1_duracao = scrapy.Field()
    fmm_design_1_descricao = scrapy.Field()
    fmm_design_1_tipo = scrapy.Field()
    fmm_design_1_tipo_perguntas_respostas_href = scrapy.Field()
    fmm_design_1_tipo_apresentacao_licao_melhore_titulo = scrapy.Field()
    fmm_design_1_tipo_apresentacao_licao_melhore_href = scrapy.Field()

    fmm_design_2_titulo = scrapy.Field()
    fmm_design_2_duracao = scrapy.Field()
    fmm_design_2_descricao = scrapy.Field()
    fmm_design_2_tipo = scrapy.Field()
    fmm_design_2_tipo_perguntas_respostas_href = scrapy.Field()
    fmm_design_2_tipo_apresentacao_licao_melhore_titulo = scrapy.Field()
    fmm_design_2_tipo_apresentacao_licao_melhore_href = scrapy.Field()

    fmm_design_3_titulo = scrapy.Field()
    fmm_design_3_duracao = scrapy.Field()
    fmm_design_3_descricao = scrapy.Field()
    fmm_design_3_tipo = scrapy.Field()
    fmm_design_3_tipo_perguntas_respostas_href = scrapy.Field()
    fmm_design_3_tipo_apresentacao_licao_melhore_titulo = scrapy.Field()
    fmm_design_3_tipo_apresentacao_licao_melhore_href = scrapy.Field()

    fmm_design_4_titulo = scrapy.Field()
    fmm_design_4_duracao = scrapy.Field()
    fmm_design_4_descricao = scrapy.Field()
    fmm_design_4_tipo = scrapy.Field()
    fmm_design_4_tipo_perguntas_respostas_href = scrapy.Field()
    fmm_design_4_tipo_apresentacao_licao_melhore_titulo = scrapy.Field()
    fmm_design_4_tipo_apresentacao_licao_melhore_href = scrapy.Field()
    
    #Nossa vida cristã
    cantico_transicao = scrapy.Field()

    nvc_design_1_titulo = scrapy.Field()
    nvc_design_1_duracao = scrapy.Field()
    nvc_design_1_video_ou_materia_href = scrapy.Field()
    nvc_design_1_descricao = scrapy.Field()

    nvc_design_2_titulo = scrapy.Field()
    nvc_design_2_duracao = scrapy.Field()
    nvc_design_2_video_ou_materia_href = scrapy.Field()
    nvc_design_2_descricao = scrapy.Field()

    nvc_design_3_titulo = scrapy.Field()
    nvc_design_3_duracao = scrapy.Field()
    nvc_design_3_video_ou_materia_href = scrapy.Field()
    nvc_design_3_descricao = scrapy.Field()

    nvc_design_4_titulo = scrapy.Field()
    nvc_design_4_duracao = scrapy.Field()
    nvc_design_4_video_ou_materia_href = scrapy.Field()
    nvc_design_4_descricao = scrapy.Field()
    