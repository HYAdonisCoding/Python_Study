from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# 你环境里已经装了 webdriver-manager，只需要改代码，让它自动拉取和匹配版本：
options = webdriver.ChromeOptions()
options.add_argument("--headless")   # 如果需要无头模式
driver = webdriver.Chrome(
    options=options,
    executable_path=ChromeDriverManager().install()
)