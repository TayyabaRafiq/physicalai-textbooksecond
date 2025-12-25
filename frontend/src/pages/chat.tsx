import React, { useState } from 'react';
import Layout from '@theme/Layout';
import styles from './chat.module.css';

interface Source {
  module: string;
  chapter: string;
  section: string;
  chunk_id: number;
}

interface QuestionResponse {
  answer: string;
  sources: Source[];
  mode: string;
  confidence: string;
}

export default function ChatPage(): JSX.Element {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<QuestionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch('https://tayyabaali-physical-ai-backend.hf.space/api/v1/question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data: QuestionResponse = await res.json();
      setResponse(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to connect to backend. Please try again later.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion('');
    setResponse(null);
    setError(null);
  };

  return (
    <Layout
      title="Physical AI Chatbot"
      description="Ask questions about Physical AI, ROS 2, simulation, and robotics"
    >
      <div className={styles.chatContainer}>
        <div className={styles.chatHeader}>
          <h1>Physical AI Chatbot</h1>
          <p>Ask questions about Physical AI, ROS 2, simulation, and safety</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.chatForm}>
          <div className={styles.inputGroup}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What is Physical AI and how does it differ from traditional AI?"
              className={styles.input}
              disabled={loading}
            />
            <div className={styles.buttonGroup}>
              <button
                type="submit"
                className={styles.submitButton}
                disabled={loading || !question.trim()}
              >
                {loading ? 'Thinking...' : 'Ask'}
              </button>
              {(response || error) && (
                <button
                  type="button"
                  onClick={handleClear}
                  className={styles.clearButton}
                  disabled={loading}
                >
                  Clear
                </button>
              )}
            </div>
          </div>
        </form>

        {loading && (
          <div className={styles.loadingContainer}>
            <div className={styles.spinner}></div>
            <p>Searching knowledge base...</p>
          </div>
        )}

        {error && (
          <div className={styles.errorContainer}>
            <h3>⚠️ Error</h3>
            <p>{error}</p>
            <p className={styles.errorHint}>
              The backend may be experiencing issues. Please try again in a moment.
            </p>
          </div>
        )}

        {response && !loading && (
          <div className={styles.responseContainer}>
            <div className={styles.answerSection}>
              <h3>Answer</h3>
              <div className={styles.answerText}>{response.answer}</div>
              <div className={styles.metadata}>
                <span className={styles.badge}>
                  Confidence: {response.confidence}
                </span>
              </div>
            </div>

            {response.sources.length > 0 && (
              <div className={styles.sourcesSection}>
                <h3>Sources ({response.sources.length})</h3>
                <div className={styles.sourcesList}>
                  {response.sources.map((source, index) => (
                    <div key={index} className={styles.sourceCard}>
                      <div className={styles.sourceNumber}>{index + 1}</div>
                      <div className={styles.sourceDetails}>
                        <div className={styles.sourceModule}>{source.module}</div>
                        <div className={styles.sourceChapter}>{source.chapter}</div>
                        <div className={styles.sourceSection}>{source.section}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {!response && !loading && !error && (
          <div className={styles.examplesSection}>
            <h3>Example Questions</h3>
            <div className={styles.examplesList}>
              <button
                className={styles.exampleButton}
                onClick={() => setQuestion('What is Physical AI and how does it differ from traditional AI?')}
              >
                What is Physical AI and how does it differ from traditional AI?
              </button>
              <button
                className={styles.exampleButton}
                onClick={() => setQuestion('Explain the four key ROS 2 concepts: nodes, topics, services, and actions.')}
              >
                Explain the four key ROS 2 concepts: nodes, topics, services, and actions.
              </button>
              <button
                className={styles.exampleButton}
                onClick={() => setQuestion('Why is simulation important for Physical AI development?')}
              >
                Why is simulation important for Physical AI development?
              </button>
              <button
                className={styles.exampleButton}
                onClick={() => setQuestion('What are the main safety considerations for deploying Physical AI systems?')}
              >
                What are the main safety considerations for deploying Physical AI systems?
              </button>
              <button
                className={styles.exampleButton}
                onClick={() => setQuestion('How does ROS 2 use DDS for real-time communication?')}
              >
                How does ROS 2 use DDS for real-time communication?
              </button>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
