import pandas as pd
import pymysql
import sqlalchemy
from aimodule.db.config import make_data_source
import typing as t
import random
import string


class DataSource:
    def __init__(self, db_info: t.dict[str, t.Any], db_name: str):
        """
        database_uri 생성 및 sqlalchemy engine 생성
        Args:
            db_info(str): 사용할 데이터베이스 서버 정보
            db_name(str): 사용할 데이터베이스 이름
        """
        self.table_dict = {}
        # sqlalchemy
        self.database_uri = make_data_source(db_info, db_name)
        self.engine = sqlalchemy.create_engine(self.database_uri, pool_pre_ping=True)

        # pymysql
        self.conn = pymysql.connect(
            user=db_info["id"],
            passwd=db_info["pwd"],
            db=db_name,
            host=db_info["ip"],
            port=int(db_info["port"]),
            charset="utf8",
            use_unicode=True,
        )

    def __enter__(self):
        return self.engine.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.dispose()
        if self.conn:
            self.conn.close()
        print("-------------------------------" * 6)

    def __del__(self):
        if self.engine:
            self.engine.dispose()
        if self.conn:
            self.conn.close()
        print("-------------------------------" * 6)

    def df_to_sql(self, df: pd.DataFrame, table_name: str):
        """
        dataframe 형식으로 database insert
        기존의 키 값이 있을 경우 오류 발생.
        Args:
            df(DataFrame): 데이터베이스에 저장할 데이터프레임 객체
            table_name(str): 테이블 이름
        """
        print("execute start")
        df.to_sql(table_name, con=self.engine, if_exists="append", index=False)
        print("execute end")

    def table_column_names(self, table: str) -> str:
        """
        Get column names from database table
        Parameters
        ----------
        table : str
            name of the table
        Returns
        -------
        str
            names of columns as a string so we can interpolate into the SQL queries
        """
        query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
        rows = self.engine.execute(query)
        dirty_names = [i[0] for i in rows]
        clean_names = "`" + "`, `".join(map(str, dirty_names)) + "`"
        return clean_names

    def insert_conflict_ignore(self, df: pd.DataFrame, table_name: str, index: bool):
        """
        Saves dataframe to the MySQL database with 'INSERT IGNORE' query.

        First it uses pandas.to_sql to save to temporary table.
        After that it uses SQL to transfer the data to destination table, matching the columns.
        Destination table needs to exist already.
        Final step is deleting the temporary table.
        Parameters
        ----------
        df : pd.DataFrame
            dataframe to save
        table : str
            destination table name
        """
        # generate random table name for concurrent writing
        temp_table = "".join(random.choice(string.ascii_letters) for i in range(10))
        try:
            df.to_sql(temp_table, self.engine, index=index)
            columns = self.table_column_names(table=temp_table)
            insert_query = (
                f"INSERT IGNORE INTO {table_name}({columns}) SELECT {columns} FROM `{temp_table}`"
            )
            self.engine.execute(insert_query)
        except Exception as e:
            print(e)

        # drop temp table
        drop_query = f"DROP TABLE IF EXISTS `{temp_table}`"
        self.engine.execute(drop_query)

    def save_dataframe(self, df: pd.DataFrame, table_name: str):
        """
        Save dataframe to the database.
        Index is saved if it has name. If it's None it will not be saved.
        It implements INSERT IGNORE when inserting rows into the MySQL table.
        Table needs to exist before.
        Arguments:
            df {pd.DataFrame} -- dataframe to save
            table {str} -- name of the db table
        """
        if df.index.name is None:
            save_index = False
        else:
            save_index = True

        self.insert_conflict_ignore(df=df, table_name=table_name, index=save_index)

    def execute_query(self, query: str):
        """
        simply query excute
        Args:
            query(str): 실행할 쿼리
        """
        try:
            print("execute start")
            with self.engine.begin() as con:
                result = con.execute(query)
                print("execute end")
                return result
        except Exception as e:
            print(e)

    def executemany_query(self, query: str, param: list):
        """
        pymysql excutemany 대량 query 실행
        Args:
            query(str): 실행할 쿼리
            param(list): 쿼리 set, where id 파라미터

            ex) query : "update table set column=%s where id=%s;"
                param : [('김', '1'), ('이', '2')]
        """
        try:
            print("executemany start")
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                result = cursor.executemany(query, param)
                self.conn.commit()
                print("executemany end")
                return result
        except Exception as e:
            print(e)

    def select_query_to_df(self, query: str):
        """
        select 쿼리 결과를 데이터프레임 형태로 반환
        Args:
            query(str): 실행할 쿼리
        """
        try:
            print("excute start")
            df = pd.read_sql(
                query,
                con=self.engine,
            )

            print(f"df's length : {len(df)}")
            print("excute end")

        except Exception as e:
            print(e)
        return df
