from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PromptVersion:
    """
    Prompt版本号

    避免项目中直接使用字符串表示版本。
    """

    major: int

    minor: int

    patch: int = 0

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"