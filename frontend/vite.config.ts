import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import Pages from 'vite-plugin-pages'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    Pages({
        dirs: 'src/Pages',
      }),
    ],
    server: {
        proxy: {
          '/api': { // Any request starting with '/api'
            target: 'http://localhost:8000', // Your backend API server
            changeOrigin: true, // Needed for virtual hosted sites
          },
          // You can add more proxy rules for different paths if needed
          // '/auth': {
          //   target: 'http://localhost:4000',
          //   changeOrigin: true,
          //  rewrite: (path) => path.replace(/^\/auth/, ''), // Removes '/api' from the path when forwarding
          // },
        },
    },
})
