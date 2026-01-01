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

export default function ChatPage(): React.JSX.Element {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<QuestionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Helper function to safely convert any value to string
  const safeStringify = (value: any): string => {
    if (typeof value === 'string') return value;
    if (value === null || value === undefined) return '';
    if (typeof value === 'number' || typeof value === 'boolean') return String(value);
    if (typeof value === 'object') {
      // Try to extract text from common object patterns
      if (value.text) return safeStringify(value.text);
      if (value.content) return safeStringify(value.content);
      if (value.message) return safeStringify(value.message);
      if (value.answer) return safeStringify(value.answer);
      // Fallback to JSON string
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    // Handle friendly greetings and simple messages
    const lowerQuestion = question.trim().toLowerCase();
    const greetings = ['hello', 'hi', 'hey', 'hola', 'salam'];
    const thanks = ['thanks', 'thank you', 'thx', 'thankyou', 'shukriya', 'شکریہ'];

    if (greetings.some(g => lowerQuestion === g || lowerQuestion.startsWith(g + ' '))) {
      setResponse({
        answer: "Hello! 👋 I'm your Physical AI & Robotics assistant. I can help you with questions about Physical AI, ROS 2, simulation, humanoid robotics, and safety. Feel free to ask me anything!",
        sources: [],
        mode: 'greeting',
        confidence: 'High'
      });
      return;
    }

    if (thanks.some(t => lowerQuestion.includes(t))) {
      setResponse({
        answer: "You're welcome! 😊 Feel free to ask me more questions about Physical AI, ROS 2, or robotics anytime!",
        sources: [],
        mode: 'acknowledgment',
        confidence: 'High'
      });
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
        // Try to extract error message from response body
        let errorMessage = `HTTP error! status: ${res.status}`;
        try {
          const errorData = await res.json();

          if (errorData && typeof errorData === 'object') {
            // Check for nested detail.error object (custom error handler format)
            if (errorData.detail && typeof errorData.detail === 'object' && errorData.detail.error) {
              const errObj = errorData.detail.error;
              if (typeof errObj.message === 'string' && errObj.message.trim()) {
                errorMessage = errObj.message;
              } else if (typeof errObj.code === 'string' && errObj.code.trim()) {
                errorMessage = errObj.code;
              } else {
                errorMessage = JSON.stringify(errObj, null, 2);
              }
            }
            // Check for nested error object (HuggingFace format)
            else if (errorData.error && typeof errorData.error === 'object') {
              const errObj = errorData.error;
              if (typeof errObj.message === 'string' && errObj.message.trim()) {
                errorMessage = errObj.message;
              } else if (typeof errObj.code === 'string' && errObj.code.trim()) {
                errorMessage = errObj.code;
              } else {
                errorMessage = JSON.stringify(errObj, null, 2);
              }
            }
            // Check for FastAPI detail format (string)
            else if (typeof errorData.detail === 'string' && errorData.detail.trim()) {
              errorMessage = errorData.detail;
            }
            // Check for generic message
            else if (typeof errorData.message === 'string' && errorData.message.trim()) {
              errorMessage = errorData.message;
            }
            // Fallback: safely stringify the entire error object
            else {
              errorMessage = JSON.stringify(errorData, null, 2);
            }
          }
        } catch {
          // If parsing fails, use the status-based error message
        }
        throw new Error(errorMessage);
      }

      const data = await res.json();

      // Safely process response to ensure no [object Object] appears
      const processedResponse: QuestionResponse = {
        answer: safeStringify(data.answer),
        sources: Array.isArray(data.sources) ? data.sources : [],
        mode: safeStringify(data.mode),
        confidence: safeStringify(data.confidence)
      };

      setResponse(processedResponse);
    } catch (err) {
      // Ensure error is always a string, never [object Object]
      let errorMsg = 'Failed to connect to backend. Please try again later.';

      if (err instanceof Error) {
        errorMsg = err.message;
      } else if (typeof err === 'string') {
        errorMsg = err;
      } else if (err && typeof err === 'object') {
        errorMsg = JSON.stringify(err, null, 2);
      }

      setError(errorMsg);
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
