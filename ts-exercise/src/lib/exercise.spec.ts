import { BurstProcessor, ConversationGuard } from './exercise'

describe('ConversationGuard', () => {
  it('checkAndRegisterRun sets lock and returns false on first call', () => {
    const guard = new ConversationGuard()
    expect(guard.checkAndRegisterRun('conv-1')).toBe(false)
    expect(guard.runExists('conv-1')).toBe(true)
  })

  it('checkAndRegisterRun returns true on second call', () => {
    const guard = new ConversationGuard()
    guard.checkAndRegisterRun('conv-1')
    expect(guard.checkAndRegisterRun('conv-1')).toBe(true)
  })

  it('pushTo preserves order', () => {
    const guard = new ConversationGuard()
    guard.checkAndRegisterRun('conv-1')
    guard.pushTo('conv-1', { type: 'text', content: 'A' })
    guard.pushTo('conv-1', { type: 'text', content: 'B' })
    guard.pushTo('conv-1', { type: 'text', content: 'C' })
    const drained = guard.clearMessages('conv-1')
    expect(drained.map((msg) => msg.content)).toEqual(['A', 'B', 'C'])
  })

  it('pushTo returns false when no run exists', () => {
    const guard = new ConversationGuard()
    expect(guard.pushTo('conv-1', { type: 'text', content: 'A' })).toBe(false)
    expect(guard.clearMessages('conv-1')).toEqual([])
  })

  it('cleanupRun removes lock and burst', () => {
    const guard = new ConversationGuard()
    guard.checkAndRegisterRun('conv-1')
    guard.pushTo('conv-1', { type: 'text', content: 'A' })
    guard.cleanupRun('conv-1')
    expect(guard.runExists('conv-1')).toBe(false)
    expect(guard.clearMessages('conv-1')).toEqual([])
  })
})

describe('BurstProcessor', () => {
  it('processMessages preserves order and formats', () => {
    const processor = new BurstProcessor()
    const burstd = [
      { type: 'text', content: 'hello' },
      { type: 'button_reply', content: 'Large' },
      { type: 'location', payload: { lat: 1, lng: 2 } },
    ]
    const result = processor.processMessages(burstd)
    expect(result).toEqual([
      'customer:text:hello',
      'customer:button_reply:Large',
      "customer:location:{'lat': 1, 'lng': 2}",
    ])
  })

  it('buildInterruptionMessage includes source and tool note', () => {
    const processor = new BurstProcessor()
    const burstd = [{ type: 'text', content: 'hi' }]
    const message = processor.buildInterruptionMessage({
      burstd,
      wasTruncated: true,
      sentMessagesCount: 1,
      totalMessagesCount: 3,
      hasToolCalls: true,
    })
    expect(message).toContain('interrupted by the customer')
    expect(message).toContain('CANCELLED')
    expect(message).toContain('hi')
  })

  it('buildInterruptionMessage no truncation', () => {
    const processor = new BurstProcessor()
    const burstd = [{ type: 'text', content: 'next' }]
    const message = processor.buildInterruptionMessage({
      burstd,
      wasTruncated: false,
      sentMessagesCount: 1,
      totalMessagesCount: 1,
      hasToolCalls: false,
    })
    expect(message).toContain('Your full response was delivered')
    expect(message).toContain('next')
  })
})
