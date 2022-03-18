import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():

    # connect to pivot_db database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=pivot_db user=postgres password=password")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
