import { useState, useEffect } from 'react';
import { chatApi } from '../services/api';

export const useApi = () => {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await chatApi.getHealth();
        setHealth(data);
        setError(null);
      } catch (err) {
        setError('Cannot connect to server. Make sure the backend is running.');
        console.error('Health check failed:', err);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
    // Check every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return { health, loading, error };
};
