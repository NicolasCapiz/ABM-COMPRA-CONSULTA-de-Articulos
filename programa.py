import sqlite3
import datetime
from PaPDF import PaPDF


conn = sqlite3.connect('mydatabase.db')

conn.execute('''CREATE TABLE IF NOT EXISTS sales
 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
 item_id TEXT NOT NULL,
 cantidad INT NOT NULL,
 precio_venta FLOAT NOT NULL,
 iva FLOAT NOT NULL,
 descuento FLOAT NOT NULL,
 fecha DATE NOT NULL);''')

# conn.execute('''CREATE TABLE IF NOT EXISTS item
#  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#  name TEXT NOT NULL,
#  price INT NOT NULL);''')
# 
# conn.execute("""INSERT INTO item (id,name,price)
#       VALUES (NULL,'SIMPLE', 0.45);""")
# 
# conn.execute("""INSERT INTO item (id,name,price)
#       VALUES (NULL,'DOBLE FAZ', 0.85);""")
# 
# conn.execute("""INSERT INTO item (id,name,price)
#       VALUES (NULL,'AMPLIACION', 1.5);""")
# 
# conn.execute("""INSERT INTO item (id,name,price)
#       VALUES (NULL,'COLOR', 2.5);""")
# 
# conn.commit()



def add_articulo(name,price):
    conn.execute("""INSERT INTO item (id,name,price)
       VALUES (NULL,?,?);""",(name,price))
    conn.commit()
    
def del_articulo(ide):
    conn.execute("""DELETE FROM item WHERE id=?;""",(str(ide)))
    conn.commit()

def upd_articulo(ide,price):
    conn.execute('UPDATE item SET price=? WHERE id=?;',(str(price),str(ide)))
    conn.commit()

# def upd_articulo(ide,name,price):
#     conn.execute('UPDATE item SET name=?,price=? WHERE id=?;',(name,str(price),str(ide)))
#     conn.commit()


def consulta_articulos(fechaDesde,fechaHasta):
    aux=conn.execute('''SELECT i.name,s.item_id,SUM(s.cantidad),SUM(s.precio_venta),s.fecha
                        FROM sales as s
                        JOIN item as i ON i.id=s.item_id
                        WHERE s.fecha>=? AND s.fecha<=?
                        GROUP BY s.item_id,s.fecha
                        ORDER BY s.cantidad''',[fechaDesde,fechaHasta])
    conn.commit()
    return aux

def consulta_articulo_especifico(fechaDesde,fechaHasta,itemide):
    aux=conn.execute('''SELECT i.name,s.item_id,SUM(s.cantidad),SUM(s.precio_venta),s.fecha
                        FROM sales as s
                        JOIN item as i ON i.id=s.item_id
                        WHERE s.fecha>=? AND s.fecha<=? AND s.item_id==?
                        GROUP BY s.fecha
                        ORDER BY s.cantidad''',[fechaDesde,fechaHasta,itemide])
    conn.commit()
    return aux


def crear_pdf(archivo,tabla):
    with PaPDF(archivo) as pdf:
        linea=250
        for i in tabla:
            print('hola')
            aux = " ".join(i)
            print(aux)
            pdf.addText(15,linea,aux)
            linea-=10
        pdf.addText(15,100,tabla)
        print('hola')

tabla=consulta_articulos('2000-10-10','2022-10-10')
crear_pdf('hola.pdf',tabla)



def save_transaction(ide, qtty,desc):
    aux=conn.execute('SELECT count(*) FROM item WHERE id=?;',[str(ide)])
    iva = 21
    precio = obtenerPriceItem(ide)
    precio_venta = calcularPrecioVenta(qtty,precio,desc,iva)
    for i in aux:
        if(i[0]==1):
            insertSales(ide,qtty,precio_venta,iva,desc)

###############################
            
#            atecncion
            
###############################
def insertSales(ide,qtty,precio_venta,iva,desc):
    today = datetime.date.today()
    conn.execute("""INSERT INTO sales ( item_id, cantidad,precio_venta,iva,descuento,fecha) 
    VALUES (?,?,?,?,?,?);""",(ide,qtty,precio_venta,iva,desc,today))
    conn.commit()

def calcularPrecioVenta(qtty,precio,desc,iva):
    desc = 1-(desc/100)
    iva = 1+(iva/100)
    precioFinal = round((((precio*iva) * desc) * qtty),2)
    return precioFinal

def finalizar_compra(carrito,lista_items,desc):
    for i in carrito.keys():
        for j in lista_items:
            if str(j.get_ide())==i:
                print(i,j.get_price(), carrito[i])
                save_transaction(i,carrito[i], desc)    
    
def obtenerPriceItem(ide):
    aux=conn.execute('SELECT price FROM item WHERE id=?',[str(ide)])
    for i in aux:
        price = i[0]
    return price


class Item:
    def __init__(self,ide,name,price):
        self.set_ide(ide)
        self.set_name(name)
        self.set_price(price)
    
    def set_ide(self,ide):
        self.__ide = ide
    
    def get_ide(self):
        return self.__ide
    
    def set_name(self,name):
        self.__name = name
    
    def get_name(self):
        return self.__name
    
    def set_price(self,price):
        self.__price = price
    
    def get_price(self):
        return self.__price
    
    def __str__(self):
        msg = (self.get_name()+" $"+str(self.get_price()))
        return msg

                      
def load_items():
    lista_items = []
    crs = conn.execute("SELECT id, name, price FROM item")
    for fila in crs:
        lista_items.append(Item(fila[0],fila[1],fila[2]))
    return lista_items
    
def calcularTotal(carrito):
    total = 0
    lista_items = load_items()
    for i in carrito.keys():
        for j in lista_items:
            if j.get_ide() == int(i):
                aux = j.get_price() * carrito[i]
                total = round(total + aux,2)
    return total


# def tableHeaders():
#     tablas=[]
#     con = sqlite3.connect('mydatabase.db')
#     cursor = con.cursor()
#     aux=cursor.execute("PRAGMA table_info('sales')")
#     for i in aux:
#         tablas.append(i[1])
#     return tablas
def tableHeaders():
    tablas=['nombre','id','cantidad','precio de venta','fecha']
    return tablas



        
        
            