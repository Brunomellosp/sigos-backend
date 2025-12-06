import os
from typing import List


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if value is None or value == "":
        raise RuntimeError(f"Variável de ambiente obrigatória não definida: {key}")
    return value


def get_env_bool(key: str) -> bool:
    value = get_env(key).lower()
    if value in ("1", "true", "t", "yes", "y", "sim"):
        return True
    if value in ("0", "false", "f", "no", "n", "nao", "não"):
        return False
    raise RuntimeError(f"Valor inválido para boolean em {key}: {value}")


def get_env_list(key: str, separator: str = ",") -> List[str]:
    value = get_env(key)
    return [item.strip() for item in value.split(separator) if item.strip()]
