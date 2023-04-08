import sys

var_numero_pasaje_ida = 18
var_numero_pasaje_vuelta = 17
var_semana = 3
var_nombre = 'Juan'
var_apellido = 'Perez'
var_rut = '11111111-1'
var_email = 'example@example.com'
var_email2 = 'example@example.com'
var_telefono = '+56911111111'
var_ciudad = 'Santiago'
var_card_number_deb = '1234123412341234'
var_mes_siguiente = 0
if sys.platform.startswith("win"):
     var_src = r'C:\Users\juan\Downloads'
     var_trg = r'C:\Users\juan\Documents\pasajes'
else:
     var_src = '/home/juan/Downloads'
     var_trg = '/home/juan/Documents/pasajes'
var_url = 'http://ventaweb.pullmanflorida.cl/'
var_banco_rut = '22222222-2'
var_credito = 0
dictpasaje = {}
for i in range(1, 45):
    row = (i - 1) // 4 + 1
    col = i % 4 if i % 4 != 0 else 4
    dictpasaje[i] = f"div[{row}]/div[{col}]"
day_map = {
    '1': '01_lunes',
    '2': '02_martes',
    '3': '03_miercoles',
    '4': '04_jueves',
    '5': '05_viernes'
}
