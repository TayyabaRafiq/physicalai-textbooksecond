import React from 'react';
import Link from '@docusaurus/Link';

export default function FloatingChatButton() {
  return (
    <Link
      to="/chat"
      target="_blank"
      rel="noopener noreferrer"
      className="floating-chat-button"
      title="Ask AI about the docs"
      aria-label="Open AI Chatbot">
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ marginRight: '8px' }}>
        <path
          d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"/>
      </svg>
      Ask AI
    </Link>
  );
}
