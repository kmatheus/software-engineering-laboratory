import time
import logging
from functools import wraps
from typing import Callable, Optional

logger = logging.getLogger(__name__)

def timer(
    log_level: int = logging.INFO,
    log_args: bool = True,
    log_result: bool = True,
    logger_instance: Optional[logging.Logger] = None
) -> Callable:
    """
    Decorator para medir tempo de execução de funções e registrar em log.

    Args:
        log_level: Nível do log (logging.DEBUG, INFO, etc.)
        log_args: Se True, registra os argumentos da chamada.
        log_result: Se True, registra o resultado da função.
        logger_instance: Logger customizado (caso queira um logger específico).

    Uso:
        @timer(log_level=logging.DEBUG, log_args=False)
        def minha_funcao(x, y):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger_instance
            if logger_instance is None:
                logger_instance = logger

            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start) * 1000

                msg = f"{func.__name__} executada em {duration_ms:.2f} ms"
                if log_args:
                    msg += f" | args: {args}, kwargs: {kwargs}"
                if log_result and result is not None:
                    msg += f" | resultado: {result}"

                logger_instance.log(log_level, msg)
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000
                logger_instance.error(
                    f"{func.__name__} falhou após {duration_ms:.2f} ms | erro: {e}"
                )
                raise  # relança a exceção (ou você pode retornar um erro estruturado)
        return wrapper
    return decorator