import React, { useState } from 'react';
import ChatInterface from './components/Chat/ChatInterface';
import Sidebar from './components/Sidebar/Sidebar';
import ErrorBoundary from './components/UI/ErrorBoundary';
import { Menu } from 'lucide-react';
import Button from './components/UI/Button';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        {/* Mobile menu button */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-md"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Sidebar */}
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        {/* Main content */}
        <div className="lg:ml-64">
          <ChatInterface />
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;
