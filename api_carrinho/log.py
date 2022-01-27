"""
Este módulo exporta o objeto "log", usado para logging nos outros módulos da aplicação.
"""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs).03d %(levelname).3s [%(process)d] | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
log = logging.getLogger("__main__")
