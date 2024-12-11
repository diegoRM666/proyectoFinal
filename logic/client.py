import logic.bd as bd

class Cliente:
    def __init__(self, id_cliente=None, nombre=None, telefono=None, email=None, direccion=None, notas=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.notas = notas

    @classmethod
    def obtener_por_id(cls, id_cliente):
        """Obtiene un cliente por su ID desde la base de datos y devuelve una instancia de Cliente."""
        query = f"SELECT * FROM cliente WHERE idCliente = {id_cliente};"
        resultado = bd.consultar(query)
        if not resultado.empty:
            datos = resultado.iloc[0]
            return cls(
                id_cliente=datos['idCliente'],
                nombre=datos['nombre'],
                telefono=datos['telefono'],
                email=datos['email'],
                direccion=datos['direccion'],
                notas=datos.get('notas')
            )
        return None

    @classmethod
    def listar_todos():
        """Devuelve una lista de todos los clientes en la base de datos como instancias de Cliente."""
        query = "SELECT * FROM cliente;"
        resultados = bd.consultar(query)
        if not resultados.empty:
            return resultados
        else:
            return None

    def insertar(self):
        """Inserta un nuevo cliente en la base de datos."""
        query = f"""
        INSERT INTO cliente (nombre, telefono, email, direccion, notas)
        VALUES ('{self.nombre}', '{self.telefono}', '{self.email}', '{self.direccion}', '{self.notas}');
        """
        return bd.insertar(query)

    def actualizar(self):
        """Actualiza un cliente existente en la base de datos."""
        query = f"""
        UPDATE cliente
        SET nombre = '{self.nombre}', telefono = '{self.telefono}', email = '{self.email}',
            direccion = '{self.direccion}', notas = '{self.notas}'
        WHERE idCliente = {self.id_cliente};
        """
        return bd.actualizar(query)

    def eliminar(self):
        """Elimina un cliente de la base de datos."""
        query = f"DELETE FROM cliente WHERE idCliente = {self.id_cliente};"
        return bd.actualizar(query)

    def __str__(self):
        """Devuelve una representación legible del cliente."""
        return (
            f"Cliente [ID: {self.id_cliente}, Nombre: {self.nombre}, Teléfono: {self.telefono}, "
            f"Email: {self.email}, Dirección: {self.direccion}, Notas: {self.notas}]"
        )