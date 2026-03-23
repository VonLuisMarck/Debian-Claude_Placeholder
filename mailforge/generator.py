"""MailForge — email generation engine."""
from __future__ import annotations

import random
import re
import string
from datetime import datetime, timedelta
from typing import List, Tuple

from .templates import TEMPLATES, get_template, list_scenarios

DUMMY_DOMAIN = "https://secure-portal.net"

_LINK_PATHS = {
    "banco_urgente":          "/login/verify",
    "it_soporte_credenciales":"/password-reset",
    "paquete_entrega":        "/delivery/pay",
    "microsoft_cuenta":       "/account/recover",
    "vpn_acceso_caducado":    "/vpn/renew",
    "rrhh_nomina":            "/hr/update-account",
}

SAMPLE_VARS = {
    "usuario": ["jgarcia", "mlopez", "afernandez", "csanchez", "lmartinez"],
    "empresa": ["acmecorp", "grupobeta", "techsoluciones", "globalfirm"],
    "mes":     ["marzo", "abril", "mayo", "junio"],
}


def _token(n: int = 14) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def _random_past_datetime() -> Tuple[str, str]:
    delta = timedelta(hours=random.randint(1, 48))
    dt = datetime.utcnow() - delta
    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M")


def _dummy_url(scenario: str) -> str:
    path = _LINK_PATHS.get(scenario, "/verify")
    return f"{DUMMY_DOMAIN}{path}?ref={_token()}"


def _fill(text: str, emp: str, scenario: str) -> str:
    tracking   = "".join(random.choices(string.digits, k=10))
    fecha, hora = _random_past_datetime()
    usuario    = random.choice(SAMPLE_VARS["usuario"])
    mes        = random.choice(SAMPLE_VARS["mes"])
    fecha_lim  = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")
    link       = _dummy_url(scenario)

    return (
        text
        .replace("{tracking}",    tracking)
        .replace("{fecha}",       fecha)
        .replace("{hora}",        hora)
        .replace("{usuario}",     usuario)
        .replace("{empresa}",     emp)
        .replace("{mes}",         mes)
        .replace("{fecha_limite}", fecha_lim)
        .replace("{link}",        link)
    )


class EmailGenerator:
    def generate(self, scenario: str) -> dict:
        template = get_template(scenario)
        if not template:
            raise ValueError(f"Scenario '{scenario}' not found. Available: {list_scenarios()}")

        emp = random.choice(SAMPLE_VARS["empresa"])
        fill = lambda t: _fill(t, emp, scenario)

        return {
            "scenario":     scenario,
            "from_display": fill(template.from_display),
            "from_email":   fill(template.from_email),
            "subject":      fill(template.subject),
            "body":         fill(template.body),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def generate_html(self, scenario: str) -> str:
        return _render_html(self.generate(scenario))

    def generate_all(self) -> List[dict]:
        return [self.generate(s) for s in list_scenarios()]


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _body_to_html(body: str) -> str:
    escaped = _esc(body)
    return re.sub(r"(https?://[^\s]+)", r'<a href="\1">\1</a>', escaped)


def _render_html(data: dict) -> str:
    subject      = _esc(data["subject"])
    from_display = _esc(data["from_display"])
    from_email   = _esc(data["from_email"])
    date_str     = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    body_html    = _body_to_html(data["body"])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{subject}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:Arial,Helvetica,sans-serif;background:#f1f3f4;padding:20px}}
  .wrap{{max-width:680px;margin:0 auto;background:#fff;border-radius:8px;
         box-shadow:0 1px 4px rgba(0,0,0,.18);overflow:hidden}}
  .hdr{{padding:20px 28px 16px;border-bottom:1px solid #e0e0e0}}
  .subj{{font-size:20px;font-weight:400;color:#202124;margin-bottom:14px;line-height:1.4}}
  .meta{{font-size:13px;color:#5f6368;line-height:1.8}}
  .meta strong{{color:#202124}}
  .body{{padding:24px 28px;font-size:14px;line-height:1.75;color:#202124;white-space:pre-wrap}}
  .body a{{color:#1a73e8;text-decoration:none}}
  .body a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<div class="wrap">
  <div class="hdr">
    <div class="subj">{subject}</div>
    <div class="meta">
      <strong>{from_display}</strong> &lt;{from_email}&gt;<br>
      {date_str}
    </div>
  </div>
  <div class="body">{body_html}</div>
</div>
</body>
</html>"""
