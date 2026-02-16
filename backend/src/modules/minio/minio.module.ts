import { Global, Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as Minio from 'minio';
import { MINIO_TOKEN } from './minio.decorator';

@Global()
@Module({
  exports: [MINIO_TOKEN],
  providers: [
    {
      inject: [ConfigService],
      provide: MINIO_TOKEN,
      useFactory: (configService: ConfigService) => {
        const endPoint = configService.get<string>('MINIO_ENDPOINT');
        if (!endPoint) {
          throw new Error('Missing MINIO_ENDPOINT');
        }

        const portRaw = configService.get<string>('MINIO_PORT');
        const port = portRaw ? Number(portRaw) : undefined;
        if (port !== undefined && Number.isNaN(port)) {
          throw new Error('Invalid MINIO_PORT');
        }

        const accessKey = configService.get<string>('MINIO_ROOT_USER');
        const secretKey = configService.get<string>('MINIO_ROOT_PASSWORD');
        if (!accessKey || !secretKey) {
          throw new Error('Missing MINIO credentials');
        }

        const useSSLRaw = configService.get<string>('MINIO_USE_SSL');
        const useSSL = useSSLRaw ? useSSLRaw.toLowerCase() === 'true' : false;

        return new Minio.Client({
          endPoint,
          port,
          useSSL,
          accessKey,
          secretKey,
        });
      },
    },
  ],
})
export class MinioModule {}
