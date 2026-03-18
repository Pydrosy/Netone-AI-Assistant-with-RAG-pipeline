import { useState, useCallback, useRef, useEffect } from 'react';
import { chatApi } from '../services/api';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Send a message
  const sendMessage = useCallback(async (content) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Call API
      const response = await chatApi.sendQuery(content);
      
      // Add assistant message
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
        timestamp: new Date().toISOString(),
      };
      
      setMessages((prev) => [...prev, assistantMessage]);

      // Save to conversation history (for sidebar)
      const conversations = JSON.parse(localStorage.getItem('netone-conversations') || '[]');
      const newConversation = {
        id: Date.now(),
        title: content.slice(0, 30) + (content.length > 30 ? '...' : ''),
        date: new Date().toLocaleDateString(),
      };
      
      // Add to beginning, keep last 10
      const updated = [newConversation, ...conversations].slice(0, 10);
      localStorage.setItem('netone-conversations', JSON.stringify(updated));
      
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to get response');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Clear conversation
  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    setMessages,
    isLoading,
    error,
    sendMessage,
    clearChat,
    messagesEndRef,
  };
};
