
    CREATE TABLE TIPOUSUARIO
	(
		id INTEGER CONSTRAINT tipousuario_pk PRIMARY KEY,
		tipo VARCHAR(20) NOT NULL
	);

   	CREATE TABLE TIPOPUNTOSATENCION
	(
		id INTEGER CONSTRAINT tipopa_pk PRIMARY KEY,
		tipo VARCHAR(20) NOT NULL
	);

	CREATE TABLE TIPOIDENTIFICACION
	(
		id INTEGER CONSTRAINT tipoid_pk PRIMARY KEY,
		tipo VARCHAR(20) NOT NULL
	);

	CREATE TABLE TIPOEMPLEADO
	(
		id INTEGER CONSTRAINT tipoemp_pk PRIMARY KEY,
		tipo VARCHAR(20) NOT NULL
	);

	CREATE TABLE TIPOOPERACION
	(
		id INTEGER CONSTRAINT tipoop_pk PRIMARY KEY,
		tipo VARCHAR(20) NOT NULL
	);

   CREATE TABLE USUARIO
	(
		id INTEGER CONSTRAINT USUARIO_PK PRIMARY KEY,
        pin VARCHAR(12) NOT NULL,
        email VARCHAR(50) NOT NULL,
        tipo INTEGER NOT NULL,
        FOREIGN KEY (tipo) REFERENCES TIPOUSUARIO(id)
	);

	CREATE TABLE EMPLEADO
	(
		id INTEGER CONSTRAINT EMPLEADO_PK PRIMARY KEY,
		tipo_documento INTEGER NOT NULL, 
		num_documento VARCHAR(15) NOT NULL,
		nombre VARCHAR(30) NOT NULL,
		apellido VARCHAR(30) NOT NULL,
		direccion VARCHAR(50) NOT NULL,
		telefono VARCHAR(15) NOT NULL,
		fecha_inscripcion DATE NOT NULL,
		tipo_empleado INTEGER NOT NULL, 
		fecha_nacimiento DATE NOT NULL,
		ciudad VARCHAR(20) NOT NULL,
		departamento VARCHAR(20) NOT NULL,
		cod_postal VARCHAR(6) NOT NULL,
		oficina INTEGER,
		FOREIGN KEY (tipo_documento) REFERENCES TIPODOCUMENTO(id),
		FOREIGN KEY (tipo_empleado) REFERENCES TIPOEMPLEADO(id),
		FOREIGN KEY (oficina) REFERENCES OFICINA(id),
		CONSTRAINT empleado_documento_uq UNIQUE (num_documento),

	);

	CREATE TABLE CLIENTE
	(
		id INTEGER CONSTRAINT CLIENTE_PK PRIMARY KEY,
		tipo_documento INTEGER NOT NULL,
		num_documento VARCHAR(15) NOT NULL,
		nombre VARCHAR(30) NOT NULL,
		apellido VARCHAR(30), /*Falta CK*/
		direccion VARCHAR(50) NOT NULL,
		telefono VARCHAR(15) NOT NULL,
		fecha_inscripcion DATE NOT NULL,
		tipo_cliente INTEGER NOT NULL, 
		fecha_nacimiento DATE, /*Falta CK*/
		ciudad VARCHAR(20) NOT NULL,
		departamento VARCHAR(20) NOT NULL,
		cod_postal VARCHAR(6) NOT NULL,
		FOREIGN KEY (tipo_cliente) REFERENCES TIPOCLIENTE (id)
        CONSTRAINT cliente_documento_uq UNIQUE (num_documento)
	);

	CREATE TABLE TIPOCLIENTE
	(
		id INTEGER NOT NULL,
		tipo INTEGER NOT NULL,
		CONSTRAINT tipocliente_pk PRIMARY KEY(id, tipo)
	);

	CREATE TABLE PRESTAMO
	(
		id INTEGER CONSTRAINT PRESTAMO_PK PRIMARY KEY,
		interes DOUBLE PRECISION NOT NULL CHECK(interes >= 0),
		monto DOUBLE PRECISION NOT NULL CHECK(monto >= 0),
		vencimiento_cuota DATE NOT NULL,
		num_cuotas INTEGER NOT NULL CHECK(num_cuotas > 0),
		valor_cuota DOUBLE PRECISION NOT NULL CHECK(valor_cuota >= 0),
		tipo INTEGER NOT NULL,
		cliente INTEGER NOT NULL,
		oficina INTEGER NOT NULL,
		FOREIGN KEY (tipo) REFERENCES TIPOPRESTAMO(id),
		FOREIGN KEY (cliente) REFERENCES CLIENTE(id),
		FOREIGN KEY (oficina) REFERENCES OFICINA(id)
	);

	CREATE TABLE TIPOPRESTAMO
	(
		id INTEGER CONSTRAINT TIPOPRESTAMO_PK PRIMARY KEY,
		tipo VARCHAR(20) NOT NULL
	);

	CREATE TABLE OFICINA
	(
		id INTEGER CONSTRAINT OFICINA_PK PRIMARY KEY,
		nombre VARCHAR(60) NOT NULL,
		direccion VARCHAR(50) NOT NULL,
		telefono VARCHAR(15) NOT NULL,
		gerente INTEGER NOT NULL,
		FOREIGN KEY (gerente) REFERENCES EMPLEADO(id) 
	);

	CREATE TABLE OPERACION
	(
		numero VARCHAR(60) CONSTRAINT OPERACION_PK PRIMARY KEY,
		tipo_operacion INTEGER NOT NULL, --Falta FK
		cliente INTEGER NOT NULL, --Falta FK
		valor DOUBLE PRECISION NOT NULL,
		punto_atencion INTEGER NOT NULL, --Falta FK
		cajero INTEGER, --Falta FK
		cuenta INTEGER NOT NULL, --Falta FK
		fecha DATE NOT NULL,
		FOREIGN KEY (tipo_operacion) REFERENCES TIPOOPERACION(id),
		FOREIGN KEY (cliente) REFERENCES CLIENTE(id),
		FOREIGN KEY (punto_atencion) REFERENCES PUNTOSATENCION(id),
		FOREIGN KEY (cajero) REFERENCES EMPLEADO(id),
		FOREIGN KEY (cuenta) REFERENCES CUENTA(numero)
	);


	CREATE TABLE TIPOCUENTA
	(
		id INTEGER CONSTRAINT TIPOCUENTA_PK PRIMARY KEY,
		tipo INTEGER NOT NULL, 
	);

	CREATE TABLE CUENTA 
	(
		numero INTEGER CONSTRAINT cuenta_pk PRIMARY KEY,
		saldo DOUBLE PRECISION saldo NOT NULL,
		tipo_cuenta INTEGER,
		cliente INTEGER NOT NULL,
        oficina INTEGER NOT NULL,
        cerrada VARCHAR(2) DEFAULT 'N' NOT NULL, 
		FOREIGN KEY (tipo_cuenta) REFERENCES TIPOCUENTA (id)
		FOREIGN KEY (cliente) REFERENCES CLIENTE(id),
        FOREIGN KEY (oficina) REFERENCES OFICINA(id)	
	);

	CREATE TABLE PUNTOSATENCION
	(
		id INTEGER CONSTRAINT puntosatencion_pk PRIMARY KEY,
		localizacion INTEGER NOT NULL,
		oficina INTEGER,
		tipo INTEGER,
		FOREIGN KEY (oficina) REFERENCES OFICINA (id),
		FOREIGN KEY (tipo) REFERENCES TIPOPUNTOSATENCION (id)
	);



	CREATE TABLE PERMITEOPERACIONPA
	(
		id_puntoAtencion INTEGER NOT NULL,
		id_tipoOperacion INTEGER NOT NULL,
		FOREIGN KEY (id_puntoAtencion) REFERENCES PUNTOSATENCION (id),
		FOREIGN KEY (id_tipoOperacion) REFERENCES TIPOOPERACION (id)
	);

	CREATE TABLE PERMITEOPERACIONCU
	(
		id_tipoCuenta INTEGER,
		id_tipoOperacion INTEGER,
		FOREIGN KEY (id_tipoCuenta) REFERENCES TIPOCUENTA (id),
		FOREIGN KEY (id_tipoOperacion) REFERENCES TIPOOPERACION (id)
	);
