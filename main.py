import psycopg2
from psycopg2.sql import SQL, Identifier


def create_tab(conn):
    with conn.cursor() as cur:

        cur.execute("""
        DROP TABLE phones;
        DROP TABLE client;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40),
        last_name VARCHAR(40),
        email VARCHAR(40)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES client(id),
        phone_number INTEGER
        );
        """)
        conn.commit()
        print('таблицы созданы')
    return


def add_client(conn, name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client (name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING id, name, last_name, email;
        """, (name, last_name, email))
        print('клиент добавлен')
        print(cur.fetchone())
    return


def add_phone(conn, id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones (id, phone_number)
        VALUES (%s, %s)
        RETURNING id, phone_number;
        """, (id, phone_number))
        print('телефон добавлен')
        print(cur.fetchone())
    return


def change_client(conn, client_id, name=None, last_name=None, email=None, phone_number=None):

    with conn.cursor() as cur:
        phone = {'phone_number': phone_number}
        for arg in phone:
            if arg:
                conn.execute(SQL("UPDATE phones SET {}=%s WHERE client_id=%s;"))
        conn.execute("""
                SELECT * FROM phones
                WHERE client_id=%s;
                """, (client_id,))
        cur.fetchone()

    with conn.cursor() as cur:
        arg_list = {'name': name, "last_name": last_name, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                conn.execute(SQL("UPDATE client SET {}=%s WHERE id=%s;").format(Identifier(key)), (arg, id))
        conn.execute("""
                SELECT * FROM Client
                WHERE id=%s;
                """, (id,))
        return cur.fetchall()


def delete_phone(conn, id, phone_number):

    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE id=%s AND phone_number=%s;
        """, (id, phone_number))
        conn.commit()
        print('телефон удалён')
    return


def delete_client(conn, id):

    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE id = %s and client_id = id;
        """, (id,))
        conn.commit()

    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client
        WHERE id=%s;
        """, (id,))
        conn.commit()
        print('клиент удалён')

    return


def find_client(conn, name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM client cl
        JOIN phones ph ON cl.id = ph.id
        WHERE (name = %(name)s OR %(name)s IS NULL)
        AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
        AND (email = %(email)s OR %(email)s IS NULL)
        AND (phone_number = %(phone)s OR %(phone)s IS NULL);
        """, {'name': name, 'last_name': last_name, 'email': email, 'phone': phone_number})
        print(cur.fetchone())
    return


if __name__ == '__main__':

    with psycopg2.connect(database='database4', user='postgres', password='Python2023') as conn:
        create_tab(conn)
        add_client(conn, 'ivan', 'ivanov', 'iivanov@)gmail.com')
        add_phone(conn, 1, 781299999)
        change_client(conn, 1, 'Petr', None, 'ppetrov@)gmail.com', 781288888)
        delete_phone(conn, 1, 781288888)
        delete_client(conn, 1)
        find_client(conn, 'Petr', 'Petrov', 'ppetrov@gmail.com', 781288888)

conn.close()

