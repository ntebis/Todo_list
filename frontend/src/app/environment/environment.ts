declare global {
  interface Window {
    env: {
      apiUrl: string;
      [key: string]: string; // For other dynamic keys
    };
  }
}

export const environment = {
  apiUrl: window.env?.apiUrl || 'http://localhost:3000/api', // Default for dev
};