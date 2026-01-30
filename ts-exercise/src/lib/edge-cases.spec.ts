import { BurstProcessor, ConversationGuard } from './exercise'

describe('ConversationGuard edge cases', () => {
  it('checkAndRegisterRun clears existing burst', () => {
    const guard = new ConversationGuard()
    guard.checkAndRegisterRun('conv-1')
    guard.pushTo('conv-1', { type: 'text', content: 'A' })
    guard.cleanupRun('conv-1')
    guard.checkAndRegisterRun('conv-1')
    expect(guard.clearMessages('conv-1')).toEqual([])
  })

  it('clearMessages is idempotent', () => {
    const guard = new ConversationGuard()
    guard.checkAndRegisterRun('conv-1')
    guard.pushTo('conv-1', { type: 'text', content: 'A' })
    const first = guard.clearMessages('conv-1')
    const second = guard.clearMessages('conv-1')
    expect(first.length).toBe(1)
    expect(second).toEqual([])
  })
})

describe('BurstProcessor edge cases', () => {
  it('prefers payload over content', () => {
    const processor = new BurstProcessor()
    const result = processor.processMessages([
      { type: 'location', content: 'ignored', payload: { lat: 1 } },
    ])
    expect(result).toEqual(["customer:location:{'lat': 1}"])
  })
})
