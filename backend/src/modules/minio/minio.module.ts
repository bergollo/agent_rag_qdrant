import { Global, Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as Minio from 'minio';

@Global()
@Module({
  exports: ['MINIO_CLIENT'],
  providers: [
    {
      inject: [ConfigService],
      provide: 'MINIO_CLIENT',
      useFactory: (configService: ConfigService) => {
        return new Minio.Client({
            endPoint: configService.get<string>('MINIO_ENDPOINT'),
            port: configService.get<number>('MINIO_PORT'),
            useSSL: false, // configService.get<boolean>('MINIO_USE_SSL'),
            accessKey: configService.get<string>('MINIO_ROOT_USER'),
            secretKey: configService.get<string>('MINIO_ROOT_PASSWORD'),
        });
      },
    },
],
})
export class MinioModule {}
