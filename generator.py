"""Core password generation logic."""

from __future__ import annotations

from dataclasses import dataclass
import secrets
import string


LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/|~"


@dataclass(frozen=True)
class PasswordOptions:
    """Settings used to create a password."""

    length: int = 16
    use_lowercase: bool = True
    use_uppercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True
    exclude: str = ""
    require_each_selected_type: bool = True


def generate_password(options: PasswordOptions | None = None) -> str:
    """Generate one secure password using the supplied options."""

    options = options or PasswordOptions()
    selected_sets = _selected_character_sets(options)
    _validate_options(options, selected_sets)

    rng = secrets.SystemRandom()
    password_chars: list[str] = []

    if options.require_each_selected_type:
        password_chars.extend(rng.choice(charset) for charset in selected_sets)

    all_allowed_chars = "".join(selected_sets)
    remaining_length = options.length - len(password_chars)
    password_chars.extend(rng.choice(all_allowed_chars) for _ in range(remaining_length))
    rng.shuffle(password_chars)

    return "".join(password_chars)


def generate_passwords(count: int, options: PasswordOptions | None = None) -> list[str]:
    """Generate several secure passwords."""

    if count < 1:
        raise ValueError("Count must be at least 1.")

    return [generate_password(options) for _ in range(count)]


def _selected_character_sets(options: PasswordOptions) -> list[str]:
    exclude = set(options.exclude)
    sets: list[str] = []

    candidates = [
        (options.use_lowercase, LOWERCASE),
        (options.use_uppercase, UPPERCASE),
        (options.use_digits, DIGITS),
        (options.use_symbols, SYMBOLS),
    ]

    for enabled, characters in candidates:
        if enabled:
            filtered = "".join(character for character in characters if character not in exclude)
            sets.append(filtered)

    return sets


def _validate_options(options: PasswordOptions, selected_sets: list[str]) -> None:
    if options.length < 4:
        raise ValueError("Password length must be at least 4.")

    if not selected_sets:
        raise ValueError("Select at least one character type.")

    empty_sets = [charset for charset in selected_sets if not charset]
    if empty_sets:
        raise ValueError("Your excluded characters removed every character from one selected type.")

    if options.require_each_selected_type and options.length < len(selected_sets):
        raise ValueError(
            "Password length is too short to include every selected character type."
        )
