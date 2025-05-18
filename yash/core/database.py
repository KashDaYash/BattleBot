import sqlite3
from threading import RLock

class DynamicDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.table = None
        self.lock = RLock()

    def set_table(self, table_name):
        self.table = table_name

    def create_table(self, table_name, fields, primary_key=None):
        with self.lock:
            self.set_table(table_name)
            columns = [f"{name} {type_}" for name, type_ in fields.items()]
            if primary_key:
                columns.append(f"PRIMARY KEY ({primary_key})")
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
            self.cursor.execute(query)
            self.conn.commit()

    def column_exists(self, column_name):
        with self.lock:
            self.cursor.execute(f"PRAGMA table_info({self.table})")
            return any(row[1] == column_name for row in self.cursor.fetchall())

    def insert(self, data: dict):
        with self.lock:
            # Add missing columns dynamically
            for key, value in data.items():
                if not self.column_exists(key):
                    col_type = "INTEGER" if isinstance(value, int) else "TEXT"
                    self.cursor.execute(f"ALTER TABLE {self.table} ADD COLUMN {key} {col_type}")

            keys = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            values = tuple(data.values())
            query = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.conn.commit()

    def find_by(self, **kwargs):
        with self.lock:
            condition = ' AND '.join([f"{k} = ?" for k in kwargs.keys()])
            values = tuple(kwargs.values())
            self.cursor.execute(f"SELECT * FROM {self.table} WHERE {condition}", values)
            return self.cursor.fetchone()

    def get_all(self, limit=None):
        with self.lock:
            query = f"SELECT * FROM {self.table}"
            if limit:
                query += f" LIMIT {limit}"
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def exists(self, **kwargs):
        with self.lock:
            return self.find_by(**kwargs) is not None

    def update(self, filters: dict, data: dict):
        with self.lock:
            for key, value in data.items():
                if not self.column_exists(key):
                    col_type = "INTEGER" if isinstance(value, int) else "TEXT"
                    self.cursor.execute(f"ALTER TABLE {self.table} ADD COLUMN {key} {col_type}")

            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            filter_clause = ' AND '.join([f"{k} = ?" for k in filters.keys()])
            values = list(data.values()) + list(filters.values())
            query = f"UPDATE {self.table} SET {set_clause} WHERE {filter_clause}"
            self.cursor.execute(query, values)
            self.conn.commit()

    def delete(self, **kwargs):
        with self.lock:
            condition = ' AND '.join([f"{k} = ?" for k in kwargs.keys()])
            values = tuple(kwargs.values())
            query = f"DELETE FROM {self.table} WHERE {condition}"
            self.cursor.execute(query, values)
            self.conn.commit()

    def count(self):
        with self.lock:
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.table}")
            return self.cursor.fetchone()[0]

    def clear_table(self):
        with self.lock:
            self.cursor.execute(f"DELETE FROM {self.table}")
            self.conn.commit()

    def drop_table(self):
        with self.lock:
            self.cursor.execute(f"DROP TABLE IF EXISTS {self.table}")
            self.conn.commit()

    def list_tables(self):
        with self.lock:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in self.cursor.fetchall()]

    def get_table_schema(self, table_name=None):
        with self.lock:
            table = table_name or self.table
            self.cursor.execute(f"PRAGMA table_info({table})")
            return [(row[1], row[2]) for row in self.cursor.fetchall()]

    def get_table_schema_str(self, table_name=None):
        with self.lock:
            table = table_name or self.table
            self.cursor.execute(f"PRAGMA table_info({table})")
            rows = self.cursor.fetchall()
            if not rows:
                return f"No schema found for table: {table}"
            schema_lines = [f"Schema for table '{table}':"]
            for row in rows:
                cid, name, type_, notnull, default, pk = row
                schema_lines.append(f"  - {name} ({type_}) {'PRIMARY KEY' if pk else ''}")
            return '\n'.join(schema_lines)