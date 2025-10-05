import { Redirect } from 'expo-router';
import { useEffect, useState } from 'react';
import Splash from './splash';

export default function Index() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <Splash />;
  }

  return <Redirect href="/(auth)/login" />;
}
