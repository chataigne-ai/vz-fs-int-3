from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MessageInput:
    """Simple message container for burst handling."""

    type: str
    content: Optional[str] = None
    timestamp: Optional[str] = None
    payload: Optional[dict] = None


class ConversationGuard:
    """In-memory guard to prevent concurrent runs and handle message bursts."""

    def __init__(self, ttl_seconds: int = 120) -> None:
        self._runs: Dict[str, bool] = {}
        self._bursts: Dict[str, List[MessageInput]] = {}
        self._ttl_seconds = ttl_seconds

    def check_and_register_run(self, conversation_id: str) -> bool:
        """Return True if a run already exists, else register and return False."""
        raise NotImplementedError

    def run_exists(self, conversation_id: str) -> bool:
        """Return True if a run exists for the conversation."""
        raise NotImplementedError

    def push_to_burst(self, conversation_id: str, message: MessageInput) -> bool:
        """Push message to burst if run exists. Return True if burstd."""
        raise NotImplementedError

    def clear_burst_messages(self, conversation_id: str) -> List[MessageInput]:
        """Drain burstd messages in FIFO order."""
        raise NotImplementedError

    def cleanup_run(self, conversation_id: str) -> None:
        """Remove run + burst for a conversation."""
        raise NotImplementedError


class BurstProcessor:
    """Transforms burstd messages into instruction strings."""

    def process_messages(self, burstd: List[MessageInput]) -> List[str]:
        """Convert burstd messages into a list of instructions (preserve order)."""
        raise NotImplementedError

    def build_interruption_message(
        self,
        burstd: List[MessageInput],
        was_truncated: bool,
        sent_messages_count: int,
        total_messages_count: int,
        has_tool_calls: bool,
    ) -> str:
        """Return combined interruption message with burstd instructions."""
        raise NotImplementedError
