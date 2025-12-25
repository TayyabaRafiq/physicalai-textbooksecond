import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Learn Physical AI and Humanoid Robotics from ROS 2 to Vision-Language-Action Systems">
      <main>
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          color: 'white',
          textAlign: 'center',
          padding: '2rem'
        }}>
          <h1 style={{
            fontSize: '3.5rem',
            fontWeight: 'bold',
            marginBottom: '1rem',
            color: 'white'
          }}>
            {siteConfig.title}
          </h1>

          <p style={{
            fontSize: '1.5rem',
            marginBottom: '2rem',
            maxWidth: '800px',
            color: 'rgba(255, 255, 255, 0.95)'
          }}>
            {siteConfig.tagline}
          </p>

          <Link
            to="/docs/"
            style={{
              backgroundColor: 'white',
              color: '#667eea',
              padding: '1rem 2rem',
              borderRadius: '8px',
              fontSize: '1.2rem',
              fontWeight: 'bold',
              textDecoration: 'none',
              display: 'inline-block',
              transition: 'transform 0.2s, box-shadow 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}>
            Start Reading
          </Link>
        </div>
      </main>
    </Layout>
  );
}
