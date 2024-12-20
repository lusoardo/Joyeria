
create database Joyeria;
use Joyeria;
CREATE TABLE Cliente (
ID_Cliente int(6) PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT,
Nombre varchar(15),
Apellido varchar(30),
Telefono int (6)
);
CREATE TABLE Pedido (
ID_Pedido int(6) PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT,
Fecha date,
Factura int(6),
ID_Cliente int(6),
FOREIGN KEY(ID_Cliente) REFERENCES Cliente(ID_Cliente)
);
CREATE TABLE Producto (
ID_Producto int(6) PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT,
Precio int(6),
Tamaño varchar (10),
 Oro varchar(10), 
 Plata varchar(10)
);
CREATE TABLE Tiene (
ID_Pedido int(6),
ID_Producto int(6),
FOREIGN KEY(ID_Pedido) REFERENCES Pedido(ID_Pedido),
FOREIGN KEY(ID_Producto) REFERENCES Producto(ID_Producto)

);
INSERT INTO Cliente(Nombre,  Apellido, Telefono )
VALUES ("Lucia","Soardo", 3584239590),
		("Johan","Rollan", 3584394560),
		("Martina","Castro", 3584239378);

INSERT INTO Pedido(Fecha, Precio)
VALUES 

INSERT INTO Producto (Precio, Tamaño, Oro, Plata)
VALUES (1000,"Grande","Oro"),
(2000,"Chico","Plata"),
(50,"Mediano","Oro");


select Pedido.ID_Pedido,Pedido.Fecha,Pedido.Monto,Cliente.Nombre from pedido inner join
Cliente on Pedido.ID_Cliente = Cliente.ID_Cliente where Pedido.ID_Cliente=1;

select * from Producto where Precio > 2000;

select * from Pedido join Producto;

select * from (Pedido inner join tiene on pedido.ID_Pedido = tiene.ID_pedido) inner join
Producto;

select * from Cliente