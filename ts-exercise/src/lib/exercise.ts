export type MessageInput = {
  type: string
  content?: string
  timestamp?: string
  payload?: Record<string, unknown>
}

export class ConversationGuard {
  private runs = new Map<string, boolean>()
  private bursts = new Map<string, MessageInput[]>()

  checkAndRegisterRun(_conversationId: string): boolean {
    throw new Error('Not implemented')
  }

  runExists(_conversationId: string): boolean {
    throw new Error('Not implemented')
  }

  pushTo(_conversationId: string, _message: MessageInput): boolean {
    throw new Error('Not implemented')
  }

  clearMessages(_conversationId: string): MessageInput[] {
    throw new Error('Not implemented')
  }

  cleanupRun(_conversationId: string): void {
    throw new Error('Not implemented')
  }
}

export class BurstProcessor {
  processMessages(_burstd: MessageInput[]): string[] {
    throw new Error('Not implemented')
  }

  buildInterruptionMessage(_args: {
    burstd: MessageInput[]
    wasTruncated: boolean
    sentMessagesCount: number
    totalMessagesCount: number
    hasToolCalls: boolean
  }): string {
    throw new Error('Not implemented')
  }
}
