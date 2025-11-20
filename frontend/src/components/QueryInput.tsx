'use client'

import { useState } from 'react'

interface QueryInputProps {
  onSubmit: (question: string) => void
  loading: boolean
}

export default function QueryInput({ onSubmit, loading }: QueryInputProps) {
  const [question, setQuestion] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (question.trim()) {
      onSubmit(question.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mb-8">
      <div className="flex gap-3">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your data..."
          className="input flex-1"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="btn-primary px-8"
        >
          {loading ? 'Processing...' : 'Ask'}
        </button>
      </div>
    </form>
  )
}
