import typing as t
from urllib.parse import quote


def make_data_source(db_info: t.Dict[str, t.Any], db_name: str):
    """
    Args:
        database_uri 생성 및 sqlalchemy engine 생성
        Args:
            db_info(str): 사용할 데이터베이스 서버 정보
            db_name(str): 사용할 데이터베이스 이름
    Returns:
        str: data_source
    """
    assert "id" in db_info
    assert "ip" in db_info
    assert "pwd" in db_info
    assert "port" in db_info
    assert db_name

    db_id = db_info["id"]
    password = db_info["pwd"]
    host = db_info["ip"]
    port = db_info["port"]

    data_source = (
        "mysql+pymysql://"
        + db_id
        + ":"
        + quote(password)
        + "@"
        + host
        + ":"
        + str(port)
        + "/"
        + db_name
    )
    return data_source
