import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Basic CSS reset and styles
const styles = `
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #f3f4f6;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  /* Simple utility classes */
  .text-center { text-align: center; }
  .text-left { text-align: left; }
  .text-right { text-align: right; }
  
  .font-bold { font-weight: bold; }
  .font-medium { font-weight: 500; }
  
  .text-sm { font-size: 14px; }
  .text-lg { font-size: 18px; }
  .text-xl { font-size: 20px; }
  .text-2xl { font-size: 24px; }
  .text-3xl { font-size: 30px; }
  
  .mb-2 { margin-bottom: 8px; }
  .mb-4 { margin-bottom: 16px; }
  .mb-6 { margin-bottom: 24px; }
  .mb-8 { margin-bottom: 32px; }
  
  .mt-1 { margin-top: 4px; }
  .mt-2 { margin-top: 8px; }
  .mt-4 { margin-top: 16px; }
  .mt-6 { margin-top: 24px; }
  .mt-8 { margin-top: 32px; }
  .mt-12 { margin-top: 48px; }
  
  .p-3 { padding: 12px; }
  .p-4 { padding: 16px; }
  .p-6 { padding: 24px; }
  .p-8 { padding: 32px; }
  
  .px-3 { padding-left: 12px; padding-right: 12px; }
  .px-4 { padding-left: 16px; padding-right: 16px; }
  .px-6 { padding-left: 24px; padding-right: 24px; }
  .px-8 { padding-left: 32px; padding-right: 32px; }
  
  .py-1 { padding-top: 4px; padding-bottom: 4px; }
  .py-2 { padding-top: 8px; padding-bottom: 8px; }
  .py-3 { padding-top: 12px; padding-bottom: 12px; }
  .py-4 { padding-top: 16px; padding-bottom: 16px; }
  
  .space-y-1 > * + * { margin-top: 4px; }
  .space-y-2 > * + * { margin-top: 8px; }
  .space-y-4 > * + * { margin-top: 16px; }
  .space-x-4 > * + * { margin-left: 16px; }
  
  .flex { display: flex; }
  .grid { display: grid; }
  .block { display: block; }
  .inline-block { display: inline-block; }
  
  .items-center { align-items: center; }
  .justify-center { justify-content: center; }
  .justify-between { justify-content: space-between; }
  
  .w-full { width: 100%; }
  .max-w-4xl { max-width: 896px; }
  .mx-auto { margin-left: auto; margin-right: auto; }
  
  .bg-white { background-color: #ffffff; }
  .bg-gray-50 { background-color: #f9fafb; }
  .bg-gray-100 { background-color: #f3f4f6; }
  .bg-gray-200 { background-color: #e5e7eb; }
  .bg-blue-50 { background-color: #eff6ff; }
  .bg-blue-600 { background-color: #2563eb; }
  .bg-green-50 { background-color: #f0fdf4; }
  .bg-green-600 { background-color: #16a34a; }
  .bg-red-600 { background-color: #dc2626; }
  .bg-yellow-400 { background-color: #facc15; }
  
  .text-gray-500 { color: #6b7280; }
  .text-gray-600 { color: #4b5563; }
  .text-gray-700 { color: #374151; }
  .text-gray-800 { color: #1f2937; }
  .text-blue-600 { color: #2563eb; }
  .text-blue-700 { color: #1d4ed8; }
  .text-blue-800 { color: #1e40af; }
  .text-green-600 { color: #16a34a; }
  .text-green-700 { color: #15803d; }
  .text-green-800 { color: #166534; }
  .text-red-600 { color: #dc2626; }
  .text-white { color: #ffffff; }
  
  .border { border: 1px solid #e5e7eb; }
  .border-blue-200 { border-color: #bfdbfe; }
  .border-green-200 { border-color: #bbf7d0; }
  .border-gray-300 { border-color: #d1d5db; }
  
  .rounded { border-radius: 4px; }
  .rounded-md { border-radius: 6px; }
  .rounded-lg { border-radius: 8px; }
  .rounded-full { border-radius: 9999px; }
  
  .shadow-md { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
  .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
  
  .cursor-pointer { cursor: pointer; }
  .cursor-not-allowed { cursor: not-allowed; }
  
  .transition-colors { transition: color 0.15s, background-color 0.15s, border-color 0.15s; }
  .transition-all { transition: all 0.15s; }
  
  .hover\\:bg-blue-700:hover { background-color: #1d4ed8; }
  .hover\\:bg-green-700:hover { background-color: #15803d; }
  .hover\\:bg-red-700:hover { background-color: #b91c1c; }
  .hover\\:border-blue-300:hover { border-color: #93c5fd; }
  .hover\\:border-green-300:hover { border-color: #86efac; }
  .hover\\:text-yellow-400:hover { color: #facc15; }
  .hover\\:scale-105:hover { transform: scale(1.05); }
  
  .focus\\:outline-none:focus { outline: none; }
  .focus\\:ring-2:focus { box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
  .focus\\:ring-blue-500:focus { box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
  
  /* Form styles */
  input, select, textarea {
    appearance: none;
    background-color: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    line-height: 1.5;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }
  
  input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  button {
    appearance: none;
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
    transition: all 0.15s ease-in-out;
  }
  
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  @media (min-width: 768px) {
    .md\\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
    .md\\:gap-8 { gap: 2rem; }
  }
`;

// Inject styles into the document
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);