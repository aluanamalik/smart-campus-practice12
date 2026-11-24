import { defineConfig } from 'vite';
import { resolve } from 'node:path';

export default defineConfig({
  root: '.',
  build: {
    rollupOptions: {
      input: {
        home: resolve(__dirname, 'index.html'),
        code: resolve(__dirname, 'code/index.html'),
        lowcode: resolve(__dirname, 'lowcode/index.html'),
      },
    },
  },
  test: {
    include: ['code/**/*.test.js'],
  },
});
