import os
import sys
from pathlib import Path
cur_project_path= str(Path(__file__).parent.absolute().parent / 'src' )

sys.path.append(cur_project_path)
print(sys.path)

# pip3 install pshmodule test
from aimodule.db import alchemy

from aimodule.db import config as db_config

## 일반 test
# from src.pshmodule.db import alchemy


def main():
    # sql -> df
    result = alchemy.DataSource(
        db_config.db_info, "portal_news_scraper"
    ).select_query_to_df(
        "select title, content, keyword from indexing_news where id='154'"
    )
    print(result.head())

    # excutemany update
    # uquery = "update etc_news set content=%s where id=%s;"
    # param = [('null입니다.', '508268'), ('null입니다.', '508174')]

    # result = alchemy.DataSource(db_config.db_info, "news_scraper").executemany_query(
    #     uquery, param
    # )
    # print(result)


if __name__ == "__main__":
    main()
