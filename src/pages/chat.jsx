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
      console.log('Sending request to:', `${API_URL}/question`);
      console.log('Request body:', { question });

      const res = await fetch(`${API_URL}/question`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      console.log('Response status:', res.status);
      console.log('Response ok:', res.ok);

      let data;
      try {
        data = await res.json();
        console.log('Response data:', data);
      } catch (parseError) {
        console.error('Failed to parse response as JSON:', parseError);
        throw new Error(`Server returned invalid JSON (Status: ${res.status})`);
      }

      if (!res.ok) {
        const errorMsg = data.detail || data.message || data.error?.message || data.error || `Server error (${res.status})`;
        console.error('Backend error:', errorMsg);
        throw new Error(errorMsg);
      }

      // Handle response - try multiple possible field names
      const answerText = data.answer || data.response || data.data?.answer || data.result;

      if (!answerText) {
        console.error('No answer field found in response:', data);
        throw new Error('Backend returned invalid response format');
      }

      setAnswer(answerText);
    } catch (err) {
      console.error('Full error details:', err);

      // Better error messages for common issues
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        setError('Network error: Unable to connect to backend. Check CORS settings or network connection.');
      } else {
        setError(err.message || 'An unexpected error occurred');
      }
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
