from python_exercise.exercise import ConversationGuard, MessageInput


def test_check_and_register_run_sets_lock_and_returns_false_on_first_call():
    guard = ConversationGuard()
    result = guard.check_and_register_run("conv-1")
    assert result is False
    assert guard.run_exists("conv-1") is True


def test_check_and_register_run_returns_true_on_second_call():
    guard = ConversationGuard()
    guard.check_and_register_run("conv-1")
    result = guard.check_and_register_run("conv-1")
    assert result is True


def test_push_to_burst_preserves_order():
    guard = ConversationGuard()
    guard.check_and_register_run("conv-1")
    guard.push_to_burst("conv-1", MessageInput(type="text", content="A"))
    guard.push_to_burst("conv-1", MessageInput(type="text", content="B"))
    guard.push_to_burst("conv-1", MessageInput(type="text", content="C"))
    drained = guard.clear_burst_messages("conv-1")
    assert [msg.content for msg in drained] == ["A", "B", "C"]


def test_push_to_burst_returns_false_when_no_run_exists():
    guard = ConversationGuard()
    result = guard.push_to_burst("conv-1", MessageInput(type="text", content="A"))
    assert result is False
    assert guard.clear_burst_messages("conv-1") == []


def test_cleanup_run_removes_lock_and_burst():
    guard = ConversationGuard()
    guard.check_and_register_run("conv-1")
    guard.push_to_burst("conv-1", MessageInput(type="text", content="A"))
    guard.cleanup_run("conv-1")
    assert guard.run_exists("conv-1") is False
    assert guard.clear_burst_messages("conv-1") == []
