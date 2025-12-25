import React, { useState } from 'react';
import Layout from '@theme/Layout';

const API_URL = 'https://tayyabaali-physical-ai-backend.hf.space/api/v1';

export default function Chat() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const res = await fetch(`${API_URL}/question`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong');
      }

      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="AI Chatbot">
      <div style={{ maxWidth: 800, margin: '40px auto' }}>
        <h1>📘 Physical AI Chatbot</h1>

        <textarea
          rows="4"
          style={{ width: '100%', padding: 10 }}
          placeholder="Ask a question about Physical AI..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={askQuestion}
          style={{ marginTop: 10, padding: '8px 16px' }}
        >
          Ask
        </button>

        {loading && <p>Thinking…</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {answer && (
          <div style={{ marginTop: 20 }}>
            <h3>Answer</h3>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
