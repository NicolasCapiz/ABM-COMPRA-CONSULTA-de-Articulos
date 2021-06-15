from bottle import route, run, template,request
import sqlite3
import programa

conn = sqlite3.connect('mydatabase.db')


carrito = {}
    
    

@route('/')
def index():
    return template('index.html')

@route('/comprar',method='GET')
def comprar():
    global carrito
    lista_items = programa.load_items()
    datos=dict(request.GET)
    if datos != {}:
        if datos['ide'] not in carrito.keys():
            carrito[datos['ide']] = int(datos['cantidad'])
        else:
            carrito[datos['ide']] = carrito[datos['ide']] + int(datos['cantidad'])    
    total = programa.calcularTotal(carrito)
    return template('comprar.html',total=total,carrito=carrito,items=lista_items)


@route('/finalizar_compra',method='GET')
def finalizar_compra():
    global carrito
    desc=0
    lista_items = programa.load_items()
    programa.finalizar_compra(carrito,lista_items,desc)
    carrito = {}
    total = 0
    return template('comprar.html',total=total,carrito=carrito,items=lista_items)

@route('/vaciar_carrito')
def vaciar_carrito():
    global carrito
    lista_items = programa.load_items()
    carrito = {}
    total = 0
    return template('comprar.html',total=total,carrito=carrito,items=lista_items)

@route('/consultas')
def consultas():
    lista_items = programa.load_items()
    datos=dict(request.GET)
    tableHeaders = programa.tableHeaders()
    if datos and datos.values():
        if ''==datos.get('ide'):
            listItemsSales = programa.consulta_articulos(datos.get('desde'),datos.get('hasta'))
        else:
            listItemsSales = programa.consulta_articulo_especifico(datos.get('desde'),datos.get('hasta'),datos.get('ide'))
        return template('consultas.html',items=lista_items,tableHeaders=tableHeaders,listItemsSales=listItemsSales)
    else:
        listItemsSales=[]
        return template('consultas.html',items=lista_items,tableHeaders=tableHeaders,listItemsSales=listItemsSales)


@route('/administrar_articulo')
def administrar_articulo():
    lista_items = programa.load_items()
    datos=dict(request.GET)
    print(datos)
    return template('administrar_articulo.html',items=lista_items)
    
@route('/agregar_articulo',method='GET')
def agregar_articulo():
    datos=dict(request.GET)
    print(datos)
    programa.add_articulo(datos.get('name_articulo'),datos.get('price_articulo'))
    lista_items = programa.load_items()
    return template('administrar_articulo.html',items=lista_items)

@route('/eliminar_articulo',method='GET')
def eliminar_articulo():
    datos=dict(request.GET)
    print(datos)
    programa.del_articulo(datos.get('ide'))
    lista_items = programa.load_items()
    return template('administrar_articulo.html',items=lista_items)

@route('/modificar_articulo',method='GET')
def modificar_articulo():
    datos=dict(request.GET)
    print(datos)
    programa.upd_articulo(datos.get('ide'),datos.get('new_price'))
    lista_items = programa.load_items()
    return template('administrar_articulo.html',items=lista_items)

run(host='localhost', port=8080)
conn.close()
