from typing import Dict, List


class ChatMessage:
    """Represents a single chat message."""

    def __init__(self, content: str, role: str = "user"):
        self.content = content
        self.role = role

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "ChatMessage":
        return cls(content=data["content"], role=data["role"])


class ChatHistory:
    """Manages a collection of ChatMessages."""

    def __init__(self):
        self._messages: List[ChatMessage] = []

    @property
    def messages(self) -> List[ChatMessage]:
        return self._messages

    def add_message(self, message: ChatMessage):
        self._messages.append(message)

    def clear(self):
        self._messages.clear()

    def to_list(self) -> List[Dict[str, str]]:
        return [msg.to_dict() for msg in self._messages]
