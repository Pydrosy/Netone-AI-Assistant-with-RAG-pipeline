import React, { useEffect } from 'react';
import { useChat } from '../../hooks/useChat';
import { useApi } from '../../hooks/useApi';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';
import { AlertCircle, WifiOff, RefreshCw } from 'lucide-react';
import Button from '../UI/Button';

const ChatInterface = () => {
  const { messages, isLoading, error, sendMessage, clearChat, messagesEndRef, setMessages } = useChat();
  const { health, loading: healthLoading, error: apiError } = useApi();

  const isBackendConnected = health?.status === 'healthy';

  // Welcome message
  useEffect(() => {
    if (messages.length === 0 && isBackendConnected) {
      const welcomeMessage = {
        id: 'welcome',
        role: 'assistant',
        content: "👋 **Welcome to Netone Zimbabwe AI Assistant!**\n\nI'm here to help you with all Netone services and information. You can ask me about:\n\n📱 **Mobile Services** - Voice plans, SMS, and bundles\n💰 **OneMoney** - Mobile money platform\n📶 **Data Packages** - Daily, weekly, monthly bundles\n📍 **Network Coverage** - 4G/LTE in all provinces\n📞 **Customer Support** - Contact channels and service centers\n💳 **Airtime** - Recharge options and denominations\n🌍 **Roaming** - International services and rates\n\n**How can I assist you today?**",
        timestamp: new Date().toISOString(),
      };
      setMessages([welcomeMessage]);
    }
  }, [messages.length, isBackendConnected, setMessages]);

  if (healthLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Connecting to server...</p>
        </div>
      </div>
    );
  }

  if (!isBackendConnected) {
    return (
      <div className="flex items-center justify-center h-screen p-4">
        <div className="text-center max-w-md p-6 bg-red-50 rounded-lg">
          <WifiOff className="w-12 h-12 text-red-500 mx-auto" />
          <h2 className="mt-4 text-xl font-semibold text-red-700">Connection Error</h2>
          <p className="mt-2 text-red-600">
            Cannot connect to the backend server. Please make sure:
          </p>
          <ul className="mt-4 text-sm text-red-600 text-left list-disc pl-6">
            <li>The backend is running (python run.py)</li>
            <li>It's accessible at http://localhost:8000</li>
            <li>No firewall is blocking the connection</li>
          </ul>
          <Button
            onClick={() => window.location.reload()}
            variant="primary"
            className="mt-6 mx-auto"
          >
            <RefreshCw className="w-4 h-4 mr-2 inline" />
            Retry Connection
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Netone AI Assistant</h1>
          <p className="text-sm text-gray-500">
            {health?.stats?.total_documents || 0} documents • {health?.stats?.groq_model}
          </p>
        </div>
        <Button
          onClick={clearChat}
          variant="outline"
          size="sm"
        >
          New Chat
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        
        {isLoading && <TypingIndicator />}
        
        {error && (
          <div className="flex items-center gap-2 p-3 bg-red-50 text-red-700 rounded-lg">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p className="text-sm">{error}</p>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="pt-4 border-t border-gray-200">
        <MessageInput 
          onSend={sendMessage} 
          isLoading={isLoading}
          disabled={!isBackendConnected}
        />
        <p className="mt-2 text-xs text-gray-400 text-center">
          Powered by Groq • Knowledge base includes Netone Zimbabwe services
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;
