#!/usr/bin/env python3
"""
CLI para el generador de emails de phishing de entrenamiento.

Uso:
  python generate.py                        # Lista escenarios disponibles
  python generate.py --scenario banco_urgente
  python generate.py --scenario all         # Genera todos los escenarios
  python generate.py --scenario banco_urgente --format json
  python generate.py --scenario banco_urgente --format text
  python generate.py --scenario banco_urgente --save
"""

import argparse
import json
import sys

from phishing_trainer import EmailGenerator, list_scenarios


def main():
    parser = argparse.ArgumentParser(
        description="Generador de emails de phishing para entrenamiento de seguridad"
    )
    parser.add_argument(
        "--scenario",
        help="Escenario a generar ('all' para todos). Omitir para listar disponibles.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Formato de salida (default: text)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Guardar el resultado en el directorio output/",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directorio de salida (default: output/)",
    )
    args = parser.parse_args()

    generator = EmailGenerator(output_dir=args.output_dir)

    # Sin argumento: listar escenarios
    if not args.scenario:
        scenarios = list_scenarios()
        print("\nEscenarios disponibles:")
        print("-" * 40)
        for s in scenarios:
            print(f"  • {s}")
        print(f"\nUso: python generate.py --scenario <nombre>")
        print(f"     python generate.py --scenario all\n")
        return

    # Generar uno o todos
    if args.scenario == "all":
        emails = generator.generate_all()
    else:
        try:
            emails = [generator.generate(args.scenario)]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    for email in emails:
        if args.format == "json":
            output = json.dumps(email, ensure_ascii=False, indent=2)
        else:
            from phishing_trainer.generator import _render_text
            output = _render_text(email)

        print(output)
        print()

        if args.save:
            if args.format == "json":
                path = generator.save_json(email)
            else:
                path = generator.save_text(email)
            print(f"  → Guardado en: {path}")


if __name__ == "__main__":
    main()
