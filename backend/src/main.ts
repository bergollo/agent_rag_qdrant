import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  // Allow browser-based clients to interact with this backend through CORS.
  app.enableCors();
  await app.listen(process.env.PORT ?? 8080);
}
bootstrap();
