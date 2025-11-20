'use client'

interface ExampleQuestionsProps {
  onSelect: (question: string) => void
  disabled: boolean
}

const EXAMPLE_QUESTIONS = [
  'Which product has the highest TPV?',
  'How do weekdays influence TPV?',
  'Which segment has the highest average ticket?',
  'What is the most used anticipation method by businesses?',
  'Compare TPV by payment method',
  'What is the total TPV for credit card transactions?',
]

export default function ExampleQuestions({ onSelect, disabled }: ExampleQuestionsProps) {
  return (
    <div className="mb-8">
      <h3 className="text-sm font-semibold text-secondary mb-3 uppercase tracking-wide">
        Example Questions
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
        {EXAMPLE_QUESTIONS.map((question, index) => (
          <button
            key={index}
            onClick={() => onSelect(question)}
            disabled={disabled}
            className="btn-secondary text-sm text-left"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  )
}
