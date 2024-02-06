import pymysql
# Configuración de la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='gestion_sw',
    cursorclass=pymysql.cursors.DictCursor
)
