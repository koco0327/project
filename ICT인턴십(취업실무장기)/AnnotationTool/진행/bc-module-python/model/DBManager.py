import mysql.connector

# db 관리
class DBManager:
    # MySQL 데이터베이스 연결
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="121.134.228.36",
            port=3310,
            user="bc",
            password="love1357",
            database="bc_annotator"
        )

    def query_db(self, query_type, columns=None, table=None, values=None, update_data=None, condition=None, conditions=None):
        cursor = self.conn.cursor()
        if query_type == 'select':
            column_placeholders = "*"
            condition_placeholders = ""
            if columns:
                delim = ", "
                column_placeholders = delim.join(columns)
            if conditions:
                condition_placeholders = " ".join([f"AND {condition}=%s" for condition in conditions])

            query = f"SELECT {column_placeholders} FROM {table} WHERE 1=1 {condition_placeholders}"
            cursor.execute(query, values)
            result = cursor.fetchall()

            # 결과 행의 개수에 따라 튜플 형태 / 튜플 형태인 행 여러 개 포함하는 리스트 반환
            if len(result) == 1 and len(result[0]) != 1:
                return result[0]
            else:
                return result

        elif query_type == 'insert':
            query = f"INSERT INTO {table} ({columns}) VALUES (%s, %s, NOW(), %s)"
            cursor.execute(query, (values[0], values[1], values[2]))
            self.conn.commit()

        elif query_type == 'update':
            query = f"UPDATE {table} SET {update_data}=%s, LOGIN_TIME=NOW(), MAC_ADDR=%s WHERE {condition}=%s"
            cursor.execute(query, (values[0], values[1], values[2]))
            self.conn.commit()

        elif query_type == 'delete':
            query = f"DELETE FROM {table} WHERE {condition}=%s"
            cursor.execute(query, (values,))
            self.conn.commit()

        else:
            print("Invalid query type")