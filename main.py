# main.py
# Patrones: Singleton, Adapter y Observer

class ConfiguracionSistema:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.config = {
                "db_url": "sqlite:///rescate.db",
                "timeout": 30,
                "notificaciones_activas": True
            }
        return cls._instancia

    def obtener_config(self):
        return self.config


class Mascota:
    def __init__(self, nombre, especie, estado_salud="estable",
                 estado_adopcion="disponible"):
        self.nombre = nombre
        self.especie = especie
        self.estado_salud = estado_salud
        self.estado_adopcion = estado_adopcion


class Observador:
    def actualizar(self, mensaje):
        raise NotImplementedError("Debe implementar actualizar().")


class Adoptante(Observador):
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def actualizar(self, mensaje):
        print(f"[NOTIFICACIÓN] {self.nombre} ({self.email}): {mensaje}")


class APIExternaTwilio:
    def send_sms(self, to, body):
        print(f"[TWILIO SMS] Destinatario: {to} | Mensaje: {body}")


class AdaptadorNotificacion:
    def __init__(self, api_externa):
        self.api_externa = api_externa

    def enviar(self, mensaje, destinatario):
        self.api_externa.send_sms(destinatario, mensaje)


class SistemaNotificacion:
    def __init__(self, adaptador_notificacion):
        self.observadores = []
        self.adaptador_notificacion = adaptador_notificacion

    def suscribir(self, observador):
        if observador not in self.observadores:
            self.observadores.append(observador)

    def cancelar_suscripcion(self, observador):
        if observador in self.observadores:
            self.observadores.remove(observador)

    def notificar_disponibilidad(self, mascota):
        mensaje = (f"🐾 {mascota.nombre}, especie: {mascota.especie}, "
                   f"está disponible para adopción.")
        for observador in self.observadores:
            observador.actualizar(mensaje)
            self.adaptador_notificacion.enviar(mensaje, observador.email)


if __name__ == "__main__":
    configuracion_1 = ConfiguracionSistema()
    configuracion_2 = ConfiguracionSistema()

    print("=== SISTEMA DE CONTROL DE RESCATE Y ADOPCIÓN ANIMAL ===")
    print("Configuración global:", configuracion_1.obtener_config())
    print("¿Existe una única instancia Singleton?:",
          configuracion_1 is configuracion_2)

    twilio = APIExternaTwilio()
    adaptador = AdaptadorNotificacion(twilio)
    sistema = SistemaNotificacion(adaptador)

    sistema.suscribir(Adoptante("Ana Pérez", "ana@email.com"))
    sistema.suscribir(Adoptante("Luis Gómez", "luis@email.com"))

    mascota_nueva = Mascota("Luna", "Gato")
    print("\n=== NOTIFICACIÓN DE MASCOTA DISPONIBLE ===")
    sistema.notificar_disponibilidad(mascota_nueva)
5.1 Salida esperada
=== SISTEMA DE CONTROL DE RESCATE Y ADOPCIÓN ANIMAL ===
Configuración global: {'db_url': 'sqlite:///rescate.db', 'timeout': 30, 'notificaciones_activas': True}
¿Existe una única instancia Singleton?: True

=== NOTIFICACIÓN DE MASCOTA DISPONIBLE ===
[NOTIFICACIÓN] Ana Pérez (ana@email.com): 🐾 Luna, especie: Gato, está disponible para adopción.
[TWILIO SMS] Destinatario: ana@email.com | Mensaje: 🐾 Luna, especie: Gato, está disponible para adopción.
[NOTIFICACIÓN] Luis Gómez (luis@email.com): 🐾 Luna, especie: Gato, está disponible para adopción.
[TWILIO SMS] Destinatario: luis@email.com | Mensaje: 🐾 Luna, especie: Gato, está disponible para adopción.
