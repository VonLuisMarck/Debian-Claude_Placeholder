"""
Phishing email templates for security awareness training.
Each template includes the email content and annotated red flags
to help users learn to identify malicious emails.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RedFlag:
    element: str        # Qué parte del email
    description: str    # Por qué es sospechoso
    severity: str       # "alta", "media", "baja"


@dataclass
class PhishingTemplate:
    scenario: str
    from_display: str
    from_email: str
    subject: str
    body: str
    red_flags: list[RedFlag] = field(default_factory=list)


TEMPLATES: list[PhishingTemplate] = [

    PhishingTemplate(
        scenario="banco_urgente",
        from_display="Banco Santander Seguridad",
        from_email="seguridad@santander-alertas.net",
        subject="⚠️ URGENTE: Su cuenta ha sido suspendida temporalmente",
        body="""\
Estimado cliente,

Hemos detectado actividad inusual en su cuenta bancaria. Para proteger
sus fondos, hemos suspendido temporalmente el acceso.

Debe verificar su identidad en las próximas 24 HORAS o su cuenta
será cerrada permanentemente.

👉 Haga clic aquí para verificar: http://santander-verificacion-cuenta.xyz/login

Necesitará:
- Número de tarjeta completo
- PIN
- Clave de seguridad

Atentamente,
Equipo de Seguridad Santander
© 2024 Banco Santander S.A.
""",
        red_flags=[
            RedFlag("from_email", "Dominio 'santander-alertas.net' no es el oficial (santander.es)", "alta"),
            RedFlag("subject", "Urgencia artificial para presionar al usuario a actuar sin pensar", "alta"),
            RedFlag("enlace", "URL 'santander-verificacion-cuenta.xyz' es un dominio falso, no del banco", "alta"),
            RedFlag("solicitud", "Un banco NUNCA pide el PIN por email ni por ningún canal digital", "alta"),
            RedFlag("plazo", "El plazo de '24 horas' es una táctica de presión clásica de phishing", "media"),
        ]
    ),

    PhishingTemplate(
        scenario="it_soporte_credenciales",
        from_display="IT Support - Helpdesk",
        from_email="helpdesk@empresa-it-soporte.com",
        subject="Acción requerida: Actualización obligatoria de contraseña corporativa",
        body="""\
Hola,

El departamento de TI ha detectado que su contraseña corporativa
ha expirado y debe ser renovada de inmediato.

Si no actualiza su contraseña en las próximas 2 horas, perderá
acceso a todos los sistemas corporativos incluyendo email y VPN.

Acceda al portal de autoservicio para actualizar:
https://portal-empleados-actualizacion.net/password-reset

Usuario detectado: {usuario}@suempresa.com

Este es un mensaje automático del sistema. No responda a este correo.

IT Helpdesk
""",
        red_flags=[
            RedFlag("from_email", "El dominio no corresponde al dominio corporativo real de la empresa", "alta"),
            RedFlag("enlace", "URL externa no corporativa para introducir credenciales internas", "alta"),
            RedFlag("usuario", "Mostrar el email del usuario da falsa sensación de legitimidad", "media"),
            RedFlag("plazo", "'2 horas' — presión de tiempo para evitar que el usuario lo piense", "alta"),
            RedFlag("amenaza", "Amenaza de perder acceso a sistemas: táctica de miedo", "media"),
            RedFlag("no_responder", "'No responda a este correo' busca evitar que contactes al IT real", "baja"),
        ]
    ),

    PhishingTemplate(
        scenario="paquete_entrega",
        from_display="Correos - Notificación de entrega",
        from_email="notificacion@correos-entrega-es.com",
        subject="Tu paquete no pudo ser entregado — Acción necesaria",
        body="""\
Estimado destinatario,

Intentamos entregar su paquete (Nº seguimiento: ES{tracking}) el día
de hoy pero no fue posible porque nadie se encontraba en el domicilio.

Para programar una nueva entrega o recogerlo en oficina debe abonar
los gastos de gestión: 1,95 €

Pague aquí y programe su entrega:
http://correos-reentrega.net/pago?ref={tracking}

El paquete será devuelto al remitente en 72 horas si no actúa.

Correos España
""",
        red_flags=[
            RedFlag("from_email", "Dominio 'correos-entrega-es.com' no es correos.es (dominio oficial)", "alta"),
            RedFlag("enlace", "URL de pago en dominio no oficial — robo de datos de tarjeta", "alta"),
            RedFlag("pago_pequeño", "Cobro de importe pequeño (1,95€) para no levantar sospechas", "alta"),
            RedFlag("tracking", "Número de seguimiento genérico/falso para dar apariencia de legitimidad", "media"),
            RedFlag("plazo", "'72 horas' — presión para actuar sin verificar", "media"),
        ]
    ),

    PhishingTemplate(
        scenario="microsoft_cuenta",
        from_display="Microsoft Account Team",
        from_email="account-security@microsoft-alerts-account.com",
        subject="Alerta de seguridad: Inicio de sesión sospechoso en su cuenta Microsoft",
        body="""\
Cuenta de Microsoft - Alerta de Seguridad

Hemos detectado un inicio de sesión desde una ubicación inusual:

  País: Rusia
  Dispositivo: Windows PC desconocido
  Fecha/Hora: {fecha} {hora} UTC

Si NO fue usted, debe asegurar su cuenta de inmediato:

  [ PROTEGER MI CUENTA AHORA ]
  https://microsoft-account-security-alert.com/recover

Si FUE usted, puede ignorar este mensaje.

Microsoft respeta su privacidad.
© Microsoft Corporation, One Microsoft Way, Redmond, WA 98052
""",
        red_flags=[
            RedFlag("from_email", "Microsoft usa @accountprotection.microsoft.com, nunca dominios externos", "alta"),
            RedFlag("enlace", "Dominio 'microsoft-account-security-alert.com' no es microsoft.com", "alta"),
            RedFlag("pais_alarmante", "Mencionar 'Rusia' genera alarma emocional e impulso a actuar rápido", "alta"),
            RedFlag("footer", "Dirección y copyright de Microsoft copiados para dar apariencia legítima", "media"),
            RedFlag("boton_cta", "Botón llamativo '[PROTEGER MI CUENTA AHORA]' explota el miedo", "media"),
        ]
    ),

    PhishingTemplate(
        scenario="rrhh_nomina",
        from_display="Recursos Humanos",
        from_email="rrhh-nominas@{empresa}-payroll.com",
        subject="Actualización de datos bancarios para nómina de {mes}",
        body="""\
Estimado/a empleado/a,

Con motivo de la migración a nuestro nuevo sistema de nóminas, es
necesario que confirme sus datos bancarios actualizados antes del
{fecha_limite} para garantizar el cobro de su nómina de {mes}.

Acceda al portal de empleados para actualizar:
https://empleados-{empresa}-nominas.net/actualizar-cuenta

Datos a confirmar:
- IBAN completo
- Titular de la cuenta
- Entidad bancaria

Si no actualiza sus datos antes de la fecha límite, su nómina
podría retrasarse hasta el siguiente periodo.

Departamento de RRHH
""",
        red_flags=[
            RedFlag("from_email", "El dominio '{empresa}-payroll.com' no es el dominio corporativo real", "alta"),
            RedFlag("enlace", "URL externa para introducir datos bancarios — no es el portal corporativo", "alta"),
            RedFlag("datos_bancarios", "Ningún sistema legítimo pide el IBAN completo por este medio", "alta"),
            RedFlag("amenaza_nomina", "Amenaza de retraso de nómina para presionar psicológicamente", "alta"),
            RedFlag("migracion", "El pretexto de 'migración de sistema' es excusa habitual en phishing de RRHH", "media"),
        ]
    ),

]


def get_template(scenario: str) -> Optional[PhishingTemplate]:
    return next((t for t in TEMPLATES if t.scenario == scenario), None)


def list_scenarios() -> list[str]:
    return [t.scenario for t in TEMPLATES]
