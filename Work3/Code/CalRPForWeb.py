from MyLogging import logger
import json

SrcPath = "../../Work2/Src/WebPage"
MaxSize = 1915

url_dict = {
    "url": str,
    "urls": [],
    "pr": 0
}

for file_number in range(1, MaxSize):
    try:
        with open(f"{SrcPath}/web_{10}.txt", 'r', encoding="utf-8") as file:
            content = json.load(file)
            # print(content)
            # if content:

            #     print(content["url"])
    except FileNotFoundError:
        logger.warning(f"{file_number}.txt, FileNotFoundError...")
