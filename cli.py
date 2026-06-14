"""Command-line interface for the password generator."""

from __future__ import annotations

import argparse

from .generator import PasswordOptions, generate_passwords


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate secure random passwords.")
    parser.add_argument("-l", "--length", type=int, default=16, help="Password length.")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords.")
    parser.add_argument("--no-lowercase", action="store_true", help="Exclude lowercase letters.")
    parser.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase letters.")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits.")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols.")
    parser.add_argument(
        "--exclude",
        default="",
        help="Characters to remove from the generation pool, for example O0Il1.",
    )
    parser.add_argument(
        "--no-require-each",
        action="store_true",
        help="Do not force at least one character from each selected type.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    options = PasswordOptions(
        length=args.length,
        use_lowercase=not args.no_lowercase,
        use_uppercase=not args.no_uppercase,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
        exclude=args.exclude,
        require_each_selected_type=not args.no_require_each,
    )

    try:
        passwords = generate_passwords(args.count, options)
    except ValueError as error:
        parser.error(str(error))
        return 2

    for password in passwords:
        print(password)

    return 0
