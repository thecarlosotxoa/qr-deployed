import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
// dotenv last resort configuration
import dotenv from 'dotenv';

dotenv.config(); // Explicitly load .env file

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // dotenv last resort configuration
  define: {
    'process.env': process.env
  }
})


