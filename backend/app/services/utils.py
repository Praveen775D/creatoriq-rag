from typing import Any


def clean_int(value: Any) -> int:
    try:
        if value is None:
            return 0

        if isinstance(value, str):
            value = value.replace(",", "").strip()

        return int(float(value))
    except:
        return 0