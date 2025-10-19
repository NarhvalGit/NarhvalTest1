import { useMemo, useState } from 'react'

const DEFAULT_SYSTEM_PROMPT = 'Je bent een behulpzame assistent.'

export default function App() {
  const [userInput, setUserInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [model, setModel] = useState('gpt-4.1-mini')

  const conversation = useMemo(
    () => [
      { role: 'system', content: DEFAULT_SYSTEM_PROMPT },
      ...messages,
    ],
    [messages],
  )

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedInput = userInput.trim()
    if (!trimmedInput) {
      return
    }

    const userMessage = { role: 'user', content: trimmedInput }
    const requestMessages = [...conversation, userMessage]

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: requestMessages,
          model,
        }),
      })

      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`)
      }

      const data = await response.json()
      const assistantMessage = { role: 'assistant', content: data.reply }
      setMessages((current) => [...current, userMessage, assistantMessage])
      setUserInput('')
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>OpenAI Agent Demo</h1>
        <p>Stel een vraag aan de agent en ontvang een antwoord via de OpenAI API.</p>
      </header>

      <main>
        <section className="conversation" aria-live="polite">
          {messages.length === 0 ? (
            <p className="placeholder">Nog geen berichten. Stel de eerste vraag!</p>
          ) : (
            messages.map((message, index) => (
              <article key={`${message.role}-${index}`} className={`message ${message.role}`}>
                <h2>{message.role === 'user' ? 'Jij' : 'Agent'}</h2>
                <p>{message.content}</p>
              </article>
            ))
          )}
        </section>

        <form className="prompt-form" onSubmit={handleSubmit}>
          <label htmlFor="prompt">Prompt</label>
          <textarea
            id="prompt"
            name="prompt"
            placeholder="Typ je vraag hier..."
            value={userInput}
            onChange={(event) => setUserInput(event.target.value)}
            rows={4}
            disabled={isLoading}
          />

          <label htmlFor="model">Model</label>
          <select
            id="model"
            name="model"
            value={model}
            onChange={(event) => setModel(event.target.value)}
            disabled={isLoading}
          >
            <option value="gpt-4.1-mini">gpt-4.1-mini</option>
            <option value="gpt-4.1">gpt-4.1</option>
            <option value="gpt-4o-mini">gpt-4o-mini</option>
          </select>

          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Bezig...' : 'Stuur naar agent'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
      </main>
    </div>
  )
}
