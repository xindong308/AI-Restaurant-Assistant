import pymysql
from dbutils.pooled_db import PooledDB
from typing import Optional, List, Dict, Any, Union


class PyMySQLUtil:
    """
    PyMySQL 数据库操作封装工具类
    支持：单条/批量增删改查、事务、连接池、自动关闭资源
    """

    def __init__(
            self,
            host: str = "localhost",
            port: int = 3306,
            user: str = "root",
            password: str = "123456",
            database: str = "sky_take_out",
            charset: str = "utf8mb4"
    ):
        """
        初始化数据库连接池
        :param host: 数据库地址
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        :param charset: 字符集
        """
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,  # 最大连接数
            mincached=2,  # 初始化空闲连接数
            maxcached=5,  # 最大空闲连接数
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor  # 返回字典格式数据
        )

    def __get_conn(self):
        """从连接池获取连接和游标"""
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def __close(self, conn, cursor):
        """关闭游标和连接（自动归还连接池）"""
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # ==================== 查询操作 ====================
    def select_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """查询单条数据"""
        conn, cursor = self.__get_conn()
        try:
            cursor.execute(sql, params)
            return cursor.fetchone()
        finally:
            self.__close(conn, cursor)

    def select_all(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """查询多条数据"""
        conn, cursor = self.__get_conn()
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            self.__close(conn, cursor)

    def select_count(self, sql: str, params: Optional[tuple] = None) -> int:
        """查询总条数（COUNT）"""
        res = self.select_one(sql, params)
        return res.get("COUNT(*)") if res else 0

    # ==================== 增删改操作 ====================
    def execute(self, sql: str, params: Optional[tuple] = None) -> int:
        """执行单条 INSERT/UPDATE/DELETE，返回受影响行数"""
        conn, cursor = self.__get_conn()
        try:
            rows = cursor.execute(sql, params)
            conn.commit()
            return rows
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.__close(conn, cursor)

    def insert_get_id(self, sql: str, params: Optional[tuple] = None) -> int:
        """插入数据并返回自增ID"""
        conn, cursor = self.__get_conn()
        try:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.__close(conn, cursor)

    def batch_execute(self, sql: str, params_list: List[tuple]) -> int:
        """批量执行 INSERT/UPDATE/DELETE，效率更高"""
        conn, cursor = self.__get_conn()
        try:
            rows = cursor.executemany(sql, params_list)
            conn.commit()
            return rows
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.__close(conn, cursor)

    # ==================== 事务手动控制 ====================
    def begin_transaction(self):
        """开启事务"""
        conn, cursor = self.__get_conn()
        return conn, cursor

    @staticmethod
    def commit(conn):
        """提交事务"""
        conn.commit()

    @staticmethod
    def rollback(conn):
        """回滚事务"""
        conn.rollback()

    def close_transaction(self, conn, cursor):
        """关闭事务连接"""
        self.__close(conn, cursor)

# 替换成你的数据库信息
db = PyMySQLUtil(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    database="sky_take_out"
)
if __name__ == '__main__':

    res = db.select_all("select o.number,o.order_time,o.amount,o.phone,o.cancel_reason,d.name from orders as o left join order_detail as d on o.id = d.order_id where  user_id=1")
    order_info = ""
    for i in res:
        order_info += (
                "订单编号:" + i['number'] +
                " 订单时间:" + i['order_time'].strftime("%Y-%m-%d %H:%M:%S") +
                " 金额:" + str(i['amount']) +
                " 手机号:" + i['phone'] +
                " 取消原因:" + i['cancel_reason'] +
                " 菜品:" + i['name'] + "\n"
        )
    print(order_info)
    pass