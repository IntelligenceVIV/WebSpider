# @Time    : 2019/4/20 18:53
# @Author  : Noah
# @File    : splash_request.py
# @Software: PyCharm
# @description: splash example

# first run splash
#   docker run -p 8050:8050 scrapinghub/splash

import requests
from urllib.parse import quote

# lua script

# lua = """
# function main(splash, args)
#   local treat = require("treat")
#   local response = splash:http_get("http://httpbin.org/get")
#       return {
#         html = treat.as_string(response.body),
#         url = response.url,
#         status = response.status,
#       }
# end
# """

lua = """
function main(splash)
    return 'hello'
end
"""

URL = "http://localhost:8050/execute?lua_source="


def main():
    url = URL + quote(lua)
    response = requests.get(url)
    print(response.text)


if __name__ == "__main__":
    main()
