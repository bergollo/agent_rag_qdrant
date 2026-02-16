import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { HttpModule } from '@nestjs/axios';
import appConfig from './config/app.config';
import { HealthModule } from './modules/health/health.module';
import { AiModule } from './modules/ai/ai.module';
import { MinioModule } from './modules/minio/minio.module';
import { FilesModule } from './modules/files/files.module';

@Module({
  imports: [
    // Use Nest's HTTP utilities for any outbound requests the service may issue.
    HttpModule,
    // Load environment variables once, making ConfigService available app-wide.
    ConfigModule.forRoot({
      isGlobal: true,
      load: [appConfig],
      envFilePath: '.env',
    }),
    HealthModule,
    AiModule,
    MinioModule,
    FilesModule,
  ],
  controllers: [],
  providers: [],
})
export class AppModule {}
