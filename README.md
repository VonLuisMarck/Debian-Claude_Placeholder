# Phishing Trainer

Generador de emails de phishing simulados para **entrenamiento de concienciación en seguridad**.

Produce ejemplos de emails maliciosos con anotaciones educativas que explican
cada señal de alerta — sin enviar nada a ningún destinatario real.

## Uso

```bash
# Ver escenarios disponibles
python generate.py

# Generar un email de ejemplo (formato texto)
python generate.py --scenario banco_urgente

# Formato JSON (útil para integrar en otros sistemas)
python generate.py --scenario banco_urgente --format json

# Guardar en disco
python generate.py --scenario banco_urgente --save

# Generar todos los escenarios
python generate.py --scenario all --save
```

## Escenarios incluidos

| Escenario | Descripción |
|---|---|
| `banco_urgente` | Suplantación de banco con suspensión de cuenta |
| `it_soporte_credenciales` | Fake IT helpdesk pidiendo contraseña corporativa |
| `paquete_entrega` | Falsa notificación de Correos con cobro de gestión |
| `microsoft_cuenta` | Alerta falsa de inicio de sesión sospechoso en Microsoft |
| `rrhh_nomina` | Suplantación de RRHH solicitando datos bancarios para nómina |

## Estructura del output

Cada email generado incluye:

- **Email simulado**: remitente, asunto y cuerpo con variables realistas
- **Análisis educativo**: lista de red flags con severidad (alta/media/baja) y explicación
- **Metadatos**: escenario, fecha de generación, propósito declarado

## Añadir nuevos escenarios

Edita `phishing_trainer/templates.py` y añade una nueva entrada a la lista `TEMPLATES`
usando el dataclass `PhishingTemplate`.