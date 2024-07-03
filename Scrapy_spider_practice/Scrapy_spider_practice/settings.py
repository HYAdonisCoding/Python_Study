# Scrapy settings for Scrapy_spider_practice project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Scrapy_spider_practice"

SPIDER_MODULES = ["Scrapy_spider_practice.spiders"]
NEWSPIDER_MODULE = "Scrapy_spider_practice.spiders"

# 日志等级
LOG_LEVEL = 'DEBUG' #'WARNING' # DEBUG 'INFO'
# 日志文件
LOG_FILE = 'scrapy_xzqh.log'

SELENIUM_DRIVER_NAME = 'chrome'  # 或者 'firefox'
# SELENIUM_DRIVER_EXECUTABLE_PATH = '/Users/adam/Documents/Developer/environment/chromedriver-mac-x64_123/chromedriver'  # 替换为你的 ChromeDriver 路径
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # 如果你希望以无头模式运行浏览器，可以添加其他参数


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Scrapy_spider_practice (+http://www.yourdomain.com)"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True
# COOKIES_DEBUG = True  # Optional, to debug cookie handling

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'zh-CN,zh;q=0.9',
#    'Referer':'https://www.zhipin.com/web/common/security-check.html?seed=6PGHtb1rEMdrYuI1KTB3pi3OP07kf2GP3xa4bEaUe6c%3D&name=11f5a2fc&ts=1719474715694&callbackUrl=https%3A%2F%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3DJAVA%26city%3D101010100',
#    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
#    'Cookie': '__a=82614385.1719474285..1719474285.4.1.4.4; __c=1719474285; __zp_stoken__=8ed5fw5AtHBlBF2tpGhcVZHJ3wr9ZwoHDi3BsTcKybsK4Ynhdw4F3asOHwq5Pw4DDjlbCtMOIwrNawqPCsFzCncK8wrvCucKfWcKSwp%2FCo8KiwqTEo8SFwo3Dg2%2FCnsOBwp9EOhENEhMNFxscFRsNERsaHBkYGh4YGh4ZGB5ENcSGwprCtEY%2FST8zWFxbDVdlalZsUw9gU1BBQV0ZZBFBPCbDhMK8PUHDiSfDgMO6w4zDhsOGw7vDiMOBw4IXQUVBRsOBw700R2QTcxFhElINcA3DlmXDhjs1w4DClDhDQsODSEIfSz1ETEZCTkRCL0JIw49rw4I3OsOBwpg2QR1MQkZHP0RCRkU9SjZGSWQyQj0xSRYZFx4NMUvDhMKPw4bDsEJG; historyState=state; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1719474716; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1719472577,1719474290; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3DJAVA%26city%3D101010100&r=&g=&s=3&friend_source=0&s=3&friend_source=0; wd_guid=9a078035-e46b-46b9-ad85-e29d59d12956; __g=-; lastCity=101010100',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "Scrapy_spider_practice.middlewares.ScrapySpiderPracticeSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
   "Scrapy_spider_practice.middlewares.ScrapySpiderPracticeDownloaderMiddleware": 801,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # "Scrapy_spider_practice.pipelines.ScrapySpiderPracticePipeline": 300,
   # # ScrapySpiderDoubanPipeline
   # "Scrapy_spider_practice.pipelines.ScrapySpiderDoubanPipeline": 301,
   # # SQLiteMoviesPipeline
   # "Scrapy_spider_practice.pipelines.SQLiteMoviesPipeline": 303,
   # SQLiteAutosPipeline
   # ScrapySpiderAutosPipeline
   "Scrapy_spider_practice.pipelines.ScrapySpiderAutosPipeline": 304,
   "Scrapy_spider_practice.pipelines.SQLiteAutosPipeline": 305,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
