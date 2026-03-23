"""MailForge — email templates."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EmailTemplate:
    scenario: str
    from_display: str
    from_email: str
    subject: str
    body: str


TEMPLATES: List[EmailTemplate] = [

    EmailTemplate(
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

👉 Haga clic aquí para verificar: {link}

Necesitará:
- Número de tarjeta completo
- PIN
- Clave de seguridad

Atentamente,
Equipo de Seguridad Santander
© 2024 Banco Santander S.A.""",
    ),

    EmailTemplate(
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
{link}

Usuario detectado: {usuario}@suempresa.com

Este es un mensaje automático del sistema. No responda a este correo.

IT Helpdesk""",
    ),

    EmailTemplate(
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
{link}

El paquete será devuelto al remitente en 72 horas si no actúa.

Correos España""",
    ),

    EmailTemplate(
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
  {link}

Si FUE usted, puede ignorar este mensaje.

Microsoft respeta su privacidad.
© Microsoft Corporation, One Microsoft Way, Redmond, WA 98052""",
    ),

    EmailTemplate(
        scenario="vpn_acceso_caducado",
        from_display="IT Security - VPN Operations",
        from_email="vpn-ops@{empresa}-remote-access.net",
        subject="[ACCIÓN REQUERIDA] Su acceso VPN expira hoy — renueve ahora",
        body="""\
Estimado/a {usuario},

Su certificado de acceso remoto VPN corporativo expira HOY a las 23:59.

A partir de mañana no podrá conectarse a la red corporativa, lo que
afectará su acceso a unidades compartidas, sistemas internos y email.

Renueve su acceso en el portal de seguridad:

  {link}

Credenciales necesarias para completar la renovación:
  • Usuario de red (dominio\\usuario)
  • Contraseña actual
  • Código del token MFA

Si ya no necesita acceso remoto, ignore este mensaje y su cuenta
será desactivada automáticamente.

IT Security Team""",
    ),

    EmailTemplate(
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
{link}

Datos a confirmar:
- IBAN completo
- Titular de la cuenta
- Entidad bancaria

Si no actualiza sus datos antes de la fecha límite, su nómina
podría retrasarse hasta el siguiente periodo.

Departamento de RRHH""",
    ),

]


def get_template(scenario: str) -> Optional[EmailTemplate]:
    return next((t for t in TEMPLATES if t.scenario == scenario), None)


def list_scenarios() -> List[str]:
    return [t.scenario for t in TEMPLATES]
