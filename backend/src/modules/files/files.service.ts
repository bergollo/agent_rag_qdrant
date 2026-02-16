import { Injectable, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { randomUUID } from 'crypto';
import { createReadStream } from 'fs';
import * as Minio from 'minio';
import { InjectMinio } from 'src/modules/minio/minio.decorator';

@Injectable()
export class FilesService implements OnModuleInit {
  protected bucketName = 'main';

  constructor(
    @InjectMinio() private readonly minioService: Minio.Client,
    private readonly configService: ConfigService,
  ) {
    const configuredBucket = this.configService.get<string>('MINIO_BUCKET');
    if (configuredBucket) {
      this.bucketName = configuredBucket;
    }
  }

  async onModuleInit() {
    const exists = await this.minioService.bucketExists(this.bucketName);
    if (!exists) {
      await this.minioService.makeBucket(this.bucketName);
    }
  }

  async bucketsList() {
    return await this.minioService.listBuckets();
  }

  async getFile(filename: string) {
    return await this.minioService.presignedUrl(
      'GET',
      this.bucketName,
      filename,
    );
  }

  uploadFile(file: Express.Multer.File) {
    return new Promise((resolve, reject) => {
      const filename = `${randomUUID().toString()}-${file.originalname}`;
      const body =
        file.buffer ?? (file.path ? createReadStream(file.path) : null);
      if (!body) {
        reject(new Error('Upload file buffer or path not available'));
        return;
      }
      this.minioService.putObject(
        this.bucketName,
        filename,
        body,
        file.size,
        (error, objInfo) => {
          if (error) {
            reject(error);
          } else {
            resolve(objInfo);
          }
        },
      );
    });
  }
}
