import { Test, TestingModule } from '@nestjs/testing';
import { HttpService } from '@nestjs/axios';
import { HealthController } from './health.controller';
import { HealthService } from './health.service';
import * as rxjs from 'rxjs';

describe('HealthController', () => {
  let healthController: HealthController;

  // keep explicit references to the mock functions (avoids unbound-method)
  let httpGetMock: jest.Mock;
  let httpPostMock: jest.Mock;

  let httpService: HttpService;
  let healthService: HealthService;

  let firstValueFromSpy: jest.SpiedFunction<typeof rxjs.firstValueFrom>;

  beforeEach(async () => {
    httpGetMock = jest.fn();
    httpPostMock = jest.fn();

    httpService = {
      get: httpGetMock,
      post: httpPostMock,
    } as unknown as HttpService;

    healthService = {
      getPing: jest.fn(() => ({ status: 'ok', service: 'backend' })),
      getAiServiceUrl: jest.fn(() => 'http://ai_service:8080'),
    } as unknown as HealthService;

    firstValueFromSpy = jest.spyOn(rxjs, 'firstValueFrom');
    firstValueFromSpy.mockReset();

    const module: TestingModule = await Test.createTestingModule({
      controllers: [HealthController],
      providers: [
        { provide: HealthService, useValue: healthService },
        { provide: HttpService, useValue: httpService },
      ],
    }).compile();

    healthController = module.get<HealthController>(HealthController);
  });

  afterEach(() => {
    firstValueFromSpy.mockRestore();
  });

  describe('root', () => {
    it('should return a healthy status payload', () => {
      expect(healthController.getPing()).toEqual({
        status: 'ok',
        service: 'backend',
      });
    });
  });
});
