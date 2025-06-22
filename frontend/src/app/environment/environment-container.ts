declare global {
  interface Window {
    env: {
      apiUrl: string;
      [key: string]: string; // For other dynamic keys
    };
  }
}

export const environment = {
  apiUrl:'http://backend:3000',
};