from .proxies.proxies import get_proxies

SPIDER_MODULES = ["scrapyScript.spiders"]
NEWSPIDER_MODULE = "scrapyScript.spiders"


#########################
# Basic configuration
#########################

CONCURRENT_REQUESTS = 5
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
ROBOTSTXT_OBEY = False




#########################
# Proxies configuration
#########################

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

ROTATING_PROXY_PAGE_RETRY_TIMES = 9999999 # 
ROTATING_PROXY_LIST = get_proxies()




###########################
# User agent configuration
###########################


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"

DEFAULT_REQUEST_HEADERS = {
    'authority': 'https://guiaempresas.universia.es/',
    'upgrade-insecure-requests': '1',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest':' document'
}



###########################
# Middlewares configuration
###########################

DOWNLOADER_MIDDLEWARES = {
    # USERAGENTS
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,

    #PROXIES
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620
}