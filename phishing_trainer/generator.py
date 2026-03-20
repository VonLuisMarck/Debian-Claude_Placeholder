"""
Generador de emails de phishing para entrenamiento de usuarios.
Produce emails de ejemplo con anotaciones educativas — sin envío real.
"""

import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path

from .templates import PhishingTemplate, RedFlag, TEMPLATES, get_template, list_scenarios


# Variables de relleno para hacer cada email único
def _random_tracking() -> str:
    return "".join(random.choices(string.digits, k=10))


def _random_past_datetime() -> tuple[str, str]:
    delta = timedelta(hours=random.randint(1, 48))
    dt = datetime.utcnow() - delta
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


SAMPLE_VARS = {
    "usuario": ["jgarcia", "mlopez", "aferandez", "csanchez", "lmartinez"],
    "empresa": ["acmecorp", "grupobeta", "techsoluciones", "globalfirm"],
    "mes": ["marzo", "abril", "mayo", "junio"],
}


def _fill_variables(text: str, empresa: str = "") -> str:
    tracking = _random_tracking()
    fecha, hora = _random_past_datetime()
    usuario = random.choice(SAMPLE_VARS["usuario"])
    emp = empresa or random.choice(SAMPLE_VARS["empresa"])
    mes = random.choice(SAMPLE_VARS["mes"])

    # Calcular fecha límite (3 días desde hoy)
    fecha_limite = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")

    return (
        text.replace("{tracking}", tracking)
            .replace("{fecha}", fecha)
            .replace("{hora}", hora)
            .replace("{usuario}", usuario)
            .replace("{empresa}", emp)
            .replace("{mes}", mes)
            .replace("{fecha_limite}", fecha_limite)
    )


class EmailGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, scenario: str, custom_links: dict | None = None) -> dict:
        """Generates a training phishing email for the given scenario.

        Args:
            scenario: Scenario key.
            custom_links: Optional dict overriding link placeholders, e.g.
                          {"link_verificacion": "https://my-training-site.com/trap"}.
        """
        template = get_template(scenario)
        if not template:
            raise ValueError(f"Scenario '{scenario}' not found. Available: {list_scenarios()}")

        emp = random.choice(SAMPLE_VARS["empresa"])

        # Resolve links: template defaults → custom overrides → fill variables
        resolved_links = {
            key: _fill_variables(custom_links.get(key, default), emp)
            for key, default in template.links.items()
        }

        body = _fill_variables(template.body, emp)
        for key, url in resolved_links.items():
            body = body.replace("{" + key + "}", url)

        email = {
            "metadata": {
                "scenario": template.scenario,
                "generated_at": datetime.utcnow().isoformat(),
                "purpose": "SECURITY TRAINING — This is not a real email",
            },
            "email": {
                "from_display": _fill_variables(template.from_display, emp),
                "from_email": _fill_variables(template.from_email, emp),
                "subject": _fill_variables(template.subject, emp),
                "body": body,
            },
            "training": {
                "total_red_flags": len(template.red_flags),
                "red_flags": [
                    {
                        "elemento": rf.element,
                        "descripcion": _fill_variables(rf.description, emp),
                        "severidad": rf.severity,
                    }
                    for rf in template.red_flags
                ],
                "summary": _build_summary(template.red_flags),
                "links": resolved_links,
            },
        }
        return email

    def generate_all(self) -> list[dict]:
        return [self.generate(s) for s in list_scenarios()]

    def save_json(self, email: dict) -> Path:
        scenario = email["metadata"]["scenario"]
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"{scenario}_{ts}.json"
        path.write_text(json.dumps(email, ensure_ascii=False, indent=2))
        return path

    def save_text(self, email: dict) -> Path:
        scenario = email["metadata"]["scenario"]
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"{scenario}_{ts}.txt"
        path.write_text(_render_text(email))
        return path


def _build_summary(red_flags: list[RedFlag]) -> str:
    high = sum(1 for rf in red_flags if rf.severity == "alta")
    med = sum(1 for rf in red_flags if rf.severity == "media")
    low = sum(1 for rf in red_flags if rf.severity == "baja")
    parts = []
    if high:
        parts.append(f"{high} crítica(s)")
    if med:
        parts.append(f"{med} media(s)")
    if low:
        parts.append(f"{low} baja(s)")
    return "Señales de alerta: " + ", ".join(parts)


def _render_text(email: dict) -> str:
    e = email["email"]
    t = email["training"]
    lines = [
        "=" * 70,
        "  SIMULACIÓN DE PHISHING — MATERIAL DE ENTRENAMIENTO",
        "=" * 70,
        "",
        f"De:      {e['from_display']} <{e['from_email']}>",
        f"Asunto:  {e['subject']}",
        "",
        "--- CUERPO DEL EMAIL ---",
        "",
        e["body"],
        "",
        "=" * 70,
        f"  ANÁLISIS EDUCATIVO — {t['summary'].upper()}",
        "=" * 70,
        "",
    ]

    severity_icons = {"alta": "🔴", "media": "🟡", "baja": "🟢"}
    for i, rf in enumerate(t["red_flags"], 1):
        icon = severity_icons.get(rf["severidad"], "⚪")
        lines.append(f"{icon} [{rf['severidad'].upper()}] {rf['elemento'].upper()}")
        lines.append(f"   → {rf['descripcion']}")
        lines.append("")

    lines += [
        "-" * 70,
        "Este email es una simulación con fines educativos.",
        "No fue enviado a ningún destinatario real.",
        "-" * 70,
    ]
    return "\n".join(lines)
