import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <Layout
      title="Welcome"
      description="Interactive Physical AI Textbook with AI-powered chatbot"
    >
      <main className={styles.heroBanner}>
        <div className={styles.container}>
          <h1 className={styles.heroTitle}>
            Welcome to Physical AI Textbook
          </h1>
          <p className={styles.heroSubtitle}>
            Learn about Physical AI, ROS 2, robotics, simulation, and safety
            through an interactive AI-powered learning experience.
          </p>
          <div className={styles.buttons}>
            <Link
              className={styles.primaryButton}
              to="/docs/">
              Start Reading
            </Link>
            <Link
              className={styles.secondaryButton}
              to="/chat">
              Try AI Chat
            </Link>
          </div>
        </div>
      </main>
    </Layout>
  );
}
