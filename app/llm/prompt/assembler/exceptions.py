class MessageAssemblyException(Exception):
    """
    MessageAssembler基础异常。
    """


class EmptyConversationException(
    MessageAssemblyException
):
    """
    组装结果为空。
    """


class InvalidHistoryException(
    MessageAssemblyException
):
    """
    History结构非法。
    """