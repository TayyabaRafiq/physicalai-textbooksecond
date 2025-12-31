import React, { useState } from 'react';
import Layout from '@theme/Layout';

const API_URL = 'https://tayyabaali-physical-ai-backend.hf.space/api/v1';

const styles = {
  maxWidth: '900px',
  container: {
    margin: '0 auto',
    padding: '20px',
  },
  header: {
    fontSize: '2rem',
    marginBottom: '1.5rem',
    color: 'var(--ifm-heading-color)',
    textAlign: 'center',
  },
  chatCard: {
    backgroundColor: 'var(--ifm-card-background-color)',
    borderRadius: '12px',
    padding: '2rem',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    marginBottom: '2rem',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    marginBottom: '1rem',
  },
  textarea: {
    width: '100%',
    padding: '12px 16px',
    fontSize: '1rem',
    lineHeight: '1.5',
    border: '1px solid var(--ifm-color-emphasis-300)',
    borderRadius: '8px',
    fontFamily: 'inherit',
    resize: 'vertical',
    minHeight: '120px',
    boxSizing: 'border-box',
  },
  buttonContainer: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '8px',
  },
  button: {
    padding: '10px 24px',
    fontSize: '1rem',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: 'var(--ifm-color-primary)',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  buttonDisabled: {
    opacity: '0.6',
    cursor: 'not-allowed',
  },
  statusMessage: {
    padding: '12px 16px',
    borderRadius: '6px',
    marginTop: '1rem',
    fontSize: '0.95rem',
  },
  loading: {
    backgroundColor: 'var(--ifm-color-info-contrast-background)',
    color: 'var(--ifm-color-info)',
    border: '1px solid var(--ifm-color-info)',
  },
  error: {
    backgroundColor: '#fff5f5',
    color: '#c53030',
    border: '1px solid #feb2b2',
  },
  answerCard: {
    marginTop: '1.5rem',
    padding: '1.5rem',
    backgroundColor: 'var(--ifm-background-surface-color)',
    borderRadius: '8px',
    border: '1px solid var(--ifm-color-emphasis-200)',
  },
  answerTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '1rem',
    color: 'var(--ifm-heading-color)',
  },
  answerText: {
    fontSize: '1rem',
    lineHeight: '1.7',
    color: 'var(--ifm-font-color-base)',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
  },
  footer: {
    marginTop: '2rem',
    textAlign: 'center',
    fontSize: '0.875rem',
    color: 'var(--ifm-color-emphasis-600)',
  },
};

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
      console.log('Raw backend response:', data);
    } catch (parseError) {
      console.error('Failed to parse response as JSON:', parseError);
      throw new Error(`Server returned invalid JSON (Status: ${res.status})`);
    }

    if (!res.ok) {
      const errorMsg = data.detail || data.message || data.error?.message || data.error || `Server error (${res.status})`;
      console.error('Backend error:', errorMsg);
      throw new Error(errorMsg);
    }

    // Handle response safely
    let answerText = data.answer || data.response || data.data?.answer || data.result;

    let displayAnswer = '';
    if (typeof answerText === 'string') {
      displayAnswer = answerText;
    } else if (Array.isArray(answerText)) {
      displayAnswer = answerText
        .map(item => item.text || item.content || JSON.stringify(item))
        .join('\n');
    } else if (typeof answerText === 'object' && answerText !== null) {
      displayAnswer =
        answerText.text ||
        answerText.content ||
        answerText.message ||
        JSON.stringify(answerText, null, 2);
    } else {
      displayAnswer = 'No answer returned from backend';
    }

    setAnswer(displayAnswer);

  } catch (err) {
    console.error('Full error details:', err);

    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      setError('Network error: Unable to connect to backend. Check CORS or network.');
    } else {
      setError(err.message || 'An unexpected error occurred');
    }
  } finally {
    setLoading(false);
  }
};

const handleKeyPress = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      askQuestion();
    }
  };

  return (
    <Layout title="AI Chatbot">
      <div style={styles.container}>
        <h1 style={styles.header}>📘 Physical AI Chatbot</h1>

        <div style={styles.chatCard}>
          <div style={styles.inputGroup}>
            <textarea
              rows="5"
              style={styles.textarea}
              placeholder="Ask a question about Physical AI... (Ctrl+Enter to submit)"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyPress}
              disabled={loading}
              aria-label="Question input"
            />

            <div style={styles.buttonContainer}>
              <button
                onClick={askQuestion}
                style={{
                  ...styles.button,
                  ...(loading || !question.trim() ? styles.buttonDisabled : {}),
                }}
                disabled={loading || !question.trim()}
                aria-label="Submit question"
              >
                {loading ? 'Thinking...' : 'Ask'}
              </button>
            </div>
          </div>

          {loading && (
            <div style={{ ...styles.statusMessage, ...styles.loading }}>
              🤔 Processing your question...
            </div>
          )}

          {error && (
            <div style={{ ...styles.statusMessage, ...styles.error }} role="alert">
              ⚠️ {error}
            </div>
          )}

          {answer && (
            <div style={styles.answerCard}>
              <h3 style={styles.answerTitle}>💡 Answer</h3>
              <p style={styles.answerText}>{answer}</p>
            </div>
          )}
        </div>

        <div style={styles.footer}>
          <p>Powered by FastAPI + Hugging Face</p>
        </div>
      </div>
    </Layout>
  );
}