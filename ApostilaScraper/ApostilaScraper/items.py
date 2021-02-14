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
            
class ApostilaItems(scrapy.Item):
    

    href = scrapy.Field(output_processor=TakeFirst())
    descricao = scrapy.Field(input_processor= MapCompose(remover_quebra_linhas), output_processor= TakeFirst())
    mes_inicio = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_mes_inicio), output_processor= TakeFirst())
    mes_fim = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_mes_fim), output_processor= TakeFirst())
    ano_inicio = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_ano_inicio_e_fim), output_processor= TakeFirst())
    ano_fim = scrapy.Field(input_processor= MapCompose(remove_tags, remover_quebra_linhas, definir_ano_inicio_e_fim), output_processor= TakeFirst())
    programas_semana = scrapy.Field()

class ProgramaSemanaItems(scrapy.Item):

    semana_referencia = scrapy.Field()
    leitura_semana = scrapy.Field()
    cantico_inicial = scrapy.Field()
    #Tesouros da Palavra de Deus
    tpd_titulo = scrapy.Field()
    tpd_href = scrapy.Field()
    tpd_duracao = scrapy.Field()

    tpd_leitura_duracao = scrapy.Field()
    tpd_leitura_titulo = scrapy.Field()
    tpd_leitura_href = scrapy.Field()
    tpd_leitura_licao_melhore_titulo = scrapy.Field()
    tpd_leitura_licao_melhore_href = scrapy.Field()

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
    