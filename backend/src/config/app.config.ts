import { registerAs } from '@nestjs/config';

export default registerAs('app', () => ({
  port: parseInt(process.env.BACKEND_PORT || '8080', 10),
  host: process.env.BACKEND_HOST || 'localhost',
}));