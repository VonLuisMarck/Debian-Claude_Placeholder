#!/usr/bin/env python3
"""MailForge CLI — genera emails de muestra por escenario."""

import argparse
import json
import sys

from mailforge import EmailGenerator, list_scenarios
from mailforge.generator import _render_html


def main():
    parser = argparse.ArgumentParser(description="MailForge — generador de emails")
    parser.add_argument("--scenario", help="Escenario ('all' para todos). Omitir para listar.")
    parser.add_argument("--format", choices=["json", "html"], default="json")
    args = parser.parse_args()

    generator = EmailGenerator()

    if not args.scenario:
        print("\nEscenarios disponibles:")
        for s in list_scenarios():
            print(f"  • {s}")
        print(f"\nUso: python generate.py --scenario <nombre>")
        return

    scenarios = list_scenarios() if args.scenario == "all" else [args.scenario]

    for scenario in scenarios:
        try:
            data = generator.generate(scenario)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        if args.format == "html":
            print(_render_html(data))
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    main()
