from python_exercise.exercise import BurstProcessor, MessageInput


def test_process_messages_preserves_order_and_formats():
    processor = BurstProcessor()
    burstd = [
        MessageInput(type="text", content="hello"),
        MessageInput(type="button_reply", content="Large"),
        MessageInput(type="location", payload={"lat": 1.0, "lng": 2.0}),
    ]
    result = processor.process_messages(burstd)
    assert result == [
        "customer:text:hello",
        "customer:button_reply:Large",
        "customer:location:{'lat': 1.0, 'lng': 2.0}",
    ]


def test_build_interruption_message_includes_source_and_tool_note():
    processor = BurstProcessor()
    burstd = [MessageInput(type="text", content="hi")]
    msg = processor.build_interruption_message(
        burstd=burstd,
        was_truncated=True,
        sent_messages_count=1,
        total_messages_count=3,
        has_tool_calls=True,
    )
    assert "interrupted by the customer" in msg
    assert "CANCELLED" in msg
    assert "hi" in msg


def test_build_interruption_message_no_truncation():
    processor = BurstProcessor()
    burstd = [MessageInput(type="text", content="next")]
    msg = processor.build_interruption_message(
        burstd=burstd,
        was_truncated=False,
        sent_messages_count=1,
        total_messages_count=1,
        has_tool_calls=False,
    )
    assert "Your full response was delivered" in msg
    assert "next" in msg
