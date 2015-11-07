-- R1

SELECT * FROM FRECUENTAN WHERE ID_BEBEDOR = 1914
INTERSECT
SELECT * FROM FRECUENTAN WHERE FECHA_ULTIMA_VISITA >= TO_DATE('01/01/2012','dd/mm/yyyy');

SELECT * FROM
( SELECT * FROM ISIS2304221520.FRECUENTAN WHERE ID_BEBEDOR=1914)
WHERE FECHA_ULTIMA_VISITA>TO_DATE('01/01/2012','dd/mm/yyyy');

SELECT * FROM ISIS2304221520.FRECUENTAN WHERE ID_BEBEDOR=1914
AND FECHA_ULTIMA_VISITA>TO_DATE('01/01/2012','dd/mm/yyyy');


-- R2
k 
SELECT ID_BAR, HORARIO FROM 
(SELECT ID_BEBEDOR, ID_BAR, HORARIO
FROM FRECUENTAN) f
INNER JOIN
(SELECT ID FROM BEBEDORES WHERE NOMBRE =: nombre AND CIUDAD =:ciudad) b
ON b.ID = f.ID_BEBEDOR;

SELECT f.ID_BAR, f.HORARIO 
FROM FRECUENTAN f, (SELECT ID FROM BEBEDORES WHERE NOMBRE = 'Emilio Bravo') u
WHERE f.ID_BEBEDOR = u.ID;

SELECT f.ID_BAR, f.HORARIO FROM ISIS2304221520.FRECUENTAN f, ISIS2304221520.BEBEDORES b WHERE f.ID_BEBEDOR=b.ID AND b.NOMBRE =:nombre ;


--Punto 2 --
SELECT * FROM FRECUENTAN WHERE ID_BEBEDOR = 1914
INTERSECT
SELECT * FROM FRECUENTAN WHERE FECHA_ULTIMA_VISITA >= TO_DATE('01/01/2012','dd/mm/yyyy');

Para optimizar esta consulta se pensaría en crear un índice B+ sobre la última fecha de visita. Esto beneficia la consulta ya que
los registros están ordenados, y al encontrar la fecha solicitada es muy fácil tomar todos los registros que le proceden. Sin embargo,
crear un índice sobre ID_BEBEDOR no sería una buena idea, ya que este hace parte de la llave primaria de la tabla FRECUENTAN, y por
lo tanto hace también parte del índice compuesto creado por oracle.

SELECT f.ID_BAR, f.HORARIO FROM ISIS2304221520.FRECUENTAN f, ISIS2304221520.BEBEDORES b WHERE f.ID_BEBEDOR=b.ID AND b.NOMBRE = 'Emilio Bravo';

Para optimizar esta consulta, se querría un índice tipo Hash sobre los nombres de los bebedores. De esta manera, acceder al nombre 
dado sería muchísimo más rápido y así se podría acceder a su registro utilizando su ID en la tabla de FRECUENTAN, donde este hace 
parte de la llave primara y por lo tanto del índice compuesto automático de oracle.


SELECT ID_BAR, HORARIO FROM 
(
SELECT * FROM ISIS2304221520.FRECUENTAN f, ISIS2304221520.BEBEDORES b WHERE f.ID_BEBEDOR=b.ID AND b.NOMBRE =:nombre
INTERSECT
SELECT * FROM ISIS2304221520.FRECUENTAN f, ISIS2304221520.BEBEDORES b WHERE f.ID_BEBEDOR=b.ID AND b.CIUDAD =:ciudad
);