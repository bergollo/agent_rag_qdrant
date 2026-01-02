// backend/src/app.controller.ts
import {
  Body,
  Controller,
  Get,
  Post,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { FileInterceptor } from '@nestjs/platform-express';
import { firstValueFrom } from 'rxjs';
import FormData from 'form-data';
import type { Express } from 'express';
import type { AxiosResponse } from 'axios';
import { AppService } from './app.service';
import 'multer';

type HealthzResponse = {
  status: string;
  service: string;
};

type QueryResponse = {
  answer: string;
  // add more fields if your AI service returns them
};

type VectorstoreUploadResponse = unknown; // or define a real shape if you know it

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private readonly httpService: HttpService,
  ) {}

  @Get('/api/healthz')
  getPing(): object {
    return this.appService.getPing();
  }

  @Get('/api/ai/healthz')
  async getAiPing(): Promise<HealthzResponse> {
    console.log(
      `Proxying health check to AI service at ${this.appService.getAiServiceUrl()}`,
    );

    const internalUrl = `${this.appService.getAiServiceUrl()}/healthz`;

    const res: AxiosResponse<HealthzResponse> = await firstValueFrom(
      this.httpService.get<HealthzResponse>(internalUrl),
    );

    return res.data;
  }

  @Post('/api/ai/vectorstore/upload')
  @UseInterceptors(FileInterceptor('file'))
  async uploadVectorStore(
    @UploadedFile() file: Express.Multer.File,
  ): Promise<VectorstoreUploadResponse> {
    const internalServiceUrl = `${this.appService.getAiServiceUrl()}/v1/vectorstore/upload`;

    const formData = new FormData();
    formData.append('file', file.buffer, {
      filename: file.originalname,
      contentType: file.mimetype,
    });

    const res: AxiosResponse<VectorstoreUploadResponse> = await firstValueFrom(
      this.httpService.post<VectorstoreUploadResponse>(
        internalServiceUrl,
        formData,
        {
          headers: {
            ...formData.getHeaders(),
          },
        },
      ),
    );

    return res.data;
  }

  @Post('/api/ai/query')
  async queryAi(@Body('query') query: string): Promise<QueryResponse> {
    const internalUrl = `${this.appService.getAiServiceUrl()}/v1/query`;

    const res: AxiosResponse<QueryResponse> = await firstValueFrom(
      this.httpService.post<QueryResponse>(internalUrl, { query }),
    );

    return res.data;
  }
}
