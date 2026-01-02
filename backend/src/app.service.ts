import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AppService {
  // Holds the resolved base URL for the AI service so callers do not re-read config.
  private readonly AI_SERVICE_URL: string;

  constructor(private configService: ConfigService) {
    // Reading with a fallback default value if neither .env nor OS var exists
    this.AI_SERVICE_URL = this.configService.get<string>(
      'AI_SERVICE_URL',
      'http://ai_service:8080',
    );
  }

  // Allow controllers to reuse the resolved AI service endpoint.
  getAiServiceUrl(): string {
    return this.AI_SERVICE_URL;
  }

  // Mirror a simple status payload for health checks.
  getPing(): Record<string, string> {
    return { status: 'ok', service: 'backend' };
  }
}
