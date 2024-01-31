import pymysql
# Configuración de la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='arbeybachi1',
    database='gestion_sw',
    cursorclass=pymysql.cursors.DictCursor
)
