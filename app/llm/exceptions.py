
from enum import Enum
from typing import Optional, Dict, Any
import json

class LLMErrorCode(str, Enum):
    """LLM相关错误码枚举"""
    PROVIDER_NOT_FOUND = "PROVIDER_NOT_FOUND"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    TIMEOUT = "TIMEOUT"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_RESPONSE = "INVALID_RESPONSE"
    RESPONSE_PARSE_ERROR = "RESPONSE_PARSE_ERROR"
    MODEL_NOT_FOUND = "MODEL_NOT_FOUND"


class LLMException(Exception):
    """
    LLM层的基础异常类
    所有LLM相关的异常都应继承此类
    """
    def __init__(
        self,
        message: str,
        error_code: LLMErrorCode,
        original_exception: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.error_code = error_code
        self.original_exception = original_exception
        self.details = details or {}

    @property
    def is_retryable(self) -> bool:
        """
        判断此异常是否可重试
        默认为 False，子类可以根据具体情况进行重写
        """
        return False

    def __str__(self):
        base_str = super().__str__()
        if self.error_code:
            base_str = f"[{self.error_code}] {base_str}"
        if self.original_exception:
             base_str += f" (Original: {self.original_exception})"
        return base_str


class AuthenticationException(LLMException):
    """认证失败异常"""
    def __init__(self, message: str = "Authentication failed", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.AUTHENTICATION_FAILED,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 认证失败通常不应重试，需要修正凭据
        return False


class TimeoutException(LLMException):
    """请求超时异常"""
    def __init__(self, message: str = "Request timed out", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.TIMEOUT,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 超时通常可以重试
        return True


class RateLimitException(LLMException):
    """速率限制异常"""
    def __init__(self, message: str = "Rate limit exceeded", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.RATE_LIMIT_EXCEEDED,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 速率限制可以通过等待后重试
        return True


class ProviderUnavailableException(LLMException):
    """提供商不可用异常 (例如服务端错误 5xx)"""
    def __init__(self, message: str = "Provider unavailable", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.PROVIDER_UNAVAILABLE,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 服务暂时不可用可以尝试重试
        return True


class ProviderConnectionException(LLMException):
    """提供商连接异常 (例如 DNS 解析失败, SSL 握手失败, 网络中断)"""
    def __init__(self, message: str = "Failed to connect to provider", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.CONNECTION_ERROR,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 网络连接问题有时可以恢复，可以重试
        return True


class ProviderNotFoundException(LLMException):
    """提供商未找到异常"""
    def __init__(self, provider_name: str, original_exception: Optional[Exception] = None):
        message = f"Provider '{provider_name}' not found"
        super().__init__(
            message=message,
            error_code=LLMErrorCode.PROVIDER_NOT_FOUND,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 配置错误，不应重试
        return False


class ModelNotFoundException(LLMException):
    """模型未找到异常"""
    def __init__(self, model_name: str, original_exception: Optional[Exception] = None):
        message = f"Model '{model_name}' not found or not available for the provider"
        super().__init__(
            message=message,
            error_code=LLMErrorCode.MODEL_NOT_FOUND,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 模型不存在或不可用，不应重试
        return False


class InvalidRequestException(LLMException):
    """无效请求异常 (例如参数错误, 请求格式错误)"""
    def __init__(self, message: str = "Invalid request sent to provider", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.INVALID_REQUEST,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 调用方错误，不应重试，需要修正请求
        return False


class InvalidResponseException(LLMException):
    """提供商返回了无效或意外的响应 (例如，状态码 4xx 但不是客户端错误)"""
    def __init__(self, message: str = "Provider returned an invalid response", original_exception: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=LLMErrorCode.INVALID_RESPONSE,
            original_exception=original_exception
        )

    @property
    def is_retryable(self) -> bool:
        # 返回的内容不符合预期，重试可能无帮助
        return False


class ResponseParseException(LLMException):
    """解析提供商响应时发生错误 (例如，流式传输中的 JSON 解析失败)"""
    def __init__(self, raw_response: str = "", parsing_error: str = "", original_exception: Optional[Exception] = None):
        message = f"Failed to parse provider response: {parsing_error}. Raw: {raw_response[:100]}..." if len(raw_response) > 97 else f"Failed to parse provider response: {parsing_error}. Raw: {raw_response}"
        super().__init__(
            message=message,
            error_code=LLMErrorCode.RESPONSE_PARSE_ERROR,
            original_exception=original_exception,
            details={"raw_response": raw_response, "parsing_error": parsing_error}
        )

    @property
    def is_retryable(self) -> bool:
        # 解析错误是 SDK 问题，重试可能仍会失败，但如果是因为网络导致的数据损坏，可能重试有效
        # 这里默认为 False，可根据实际情况调整策略
        return False