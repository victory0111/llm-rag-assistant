from functools import wraps
from app.utils.logger import logger
import time


def log_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        logger.info(
            f"开始执行函数: {func.__name__}"
        )

        result = await func(*args, **kwargs)

        logger.info(
            f"函数执行完成: {func.__name__}"
        )

        return result

    return wrapper

def time_cost(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):

        start = time.time()

        result = await func(*args, **kwargs)

        end = time.time()

        logger.info(
            f"{func.__name__} 耗时: {(end-start):.4f}s"
        )

        return result

    return wrapper

def log_exceptions(func):
    """异常捕获与日志记录装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # 执行被装饰的异步函数
            return await func(*args, **kwargs)
        except Exception as e:
            # 记录异常日志，exc_info=True 会自动附带完整的堆栈跟踪信息
            logger.error(
                f"函数 {func.__name__} 发生异常: {str(e)}", 
                exc_info=True
            )
            raise  # 【关键】重新抛出异常，避免静默失败
    return wrapper