import { Body, Controller, Get, Param, Post, UploadedFile, UseInterceptors } from '@nestjs/common';
import { FilesService } from './files.service';
import { FileInterceptor } from '@nestjs/platform-express';

@Controller('files')
export class FilesController {
  constructor(readonly service: FilesService) {}

  @Get('buckets')
  bucketsList() {
    return this.service.bucketsList();
  }

  @Get('file-url/:name')
  getFile(@Param('name') name: string) {
    return this.service.getFile(name);
  }

  @Post('upload')
  @UseInterceptors(FileInterceptor('file'))
  uploadFile(
    @UploadedFile('file') file: Express.Multer.File,
  ) {
    // payload.file = file;
    return this.service.uploadFile(file);
  }
} 