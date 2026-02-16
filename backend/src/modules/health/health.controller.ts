// backend/src/app.controller.ts
import {
  Body,
  Controller,
  Get,
  Post,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import {
  ApiBadRequestResponse,
  ApiBody,
  ApiConsumes,
  ApiInternalServerErrorResponse,
  ApiOkResponse,
  ApiPayloadTooLargeResponse,
  ApiTags,
  ApiUnsupportedMediaTypeResponse,
  ApiUnprocessableEntityResponse,
} from '@nestjs/swagger';

import { HttpService } from '@nestjs/axios';
import { FileInterceptor } from '@nestjs/platform-express';
import { firstValueFrom } from 'rxjs';
import FormData from 'form-data';
import type { Express } from 'express';
import type { AxiosResponse } from 'axios';
import { HealthService } from './health.service';
import 'multer';

type HealthzResponse = {
  status: string;
  service: string;
};

type QueryResponse = {
  answer: string;
  // add more fields if your AI service returns them
};

@ApiTags('/api/healthz')
@Controller('healthz')
export class HealthController {
  constructor(private readonly healthService: HealthService) {}

  @Get()
  async getPing(): Promise<Record<string, any>> {
    return this.healthService.getPing();
  }
}
