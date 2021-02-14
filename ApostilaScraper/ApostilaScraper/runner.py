import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'apostila',
            '-O',
            'teste.json',
        ]
    )
except SystemExit:
    pass