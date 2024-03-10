import psycopg2

from util.connect_database import connect_to_database

def get_foods(food_type, index_list):
    if len(index_list) == 0:
        return []

    try:
        conn = connect_to_database()
        cur = conn.cursor()

        query = f"SELECT * FROM food where type_id = %s AND id IN ({', '.join(map(str, index_list))});"
        cur.execute(query, (food_type,))

        results = cur.fetchall()
        conn.commit()
    except psycopg2.Error as e:
        return
    finally:
        if conn:
            cur.close()
            conn.close()
    return results