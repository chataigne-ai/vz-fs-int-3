from python_exercise.exercise import BurstProcessor, ConversationGuard, MessageInput


def test_check_and_register_run_clears_existing_burst():
    guard = ConversationGuard()
    guard.check_and_register_run("conv-1")
    guard.push_to_burst("conv-1", MessageInput(type="text", content="A"))
    guard.cleanup_run("conv-1")
    guard.check_and_register_run("conv-1")
    assert guard.clear_burst_messages("conv-1") == []


def test_clear_burst_is_idempotent():
    guard = ConversationGuard()
    guard.check_and_register_run("conv-1")
    guard.push_to_burst("conv-1", MessageInput(type="text", content="A"))
    first = guard.clear_burst_messages("conv-1")
    second = guard.clear_burst_messages("conv-1")
    assert len(first) == 1
    assert second == []


def test_process_messages_prefers_payload_over_content():
    processor = BurstProcessor()
    burstd = [MessageInput(type="location", content="ignored", payload={"lat": 1})]
    result = processor.process_messages(burstd)
    assert result == ["customer:location:{'lat': 1}"]
