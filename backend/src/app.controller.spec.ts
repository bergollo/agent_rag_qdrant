import { Test, TestingModule } from '@nestjs/testing';
import { HttpService } from '@nestjs/axios';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import * as rxjs from 'rxjs';

describe('AppController', () => {
  let appController: AppController;

  // keep explicit references to the mock functions (avoids unbound-method)
  let httpGetMock: jest.Mock;
  let httpPostMock: jest.Mock;

  let httpService: HttpService;
  let appService: AppService;

  let firstValueFromSpy: jest.SpiedFunction<typeof rxjs.firstValueFrom>;

  beforeEach(async () => {
    httpGetMock = jest.fn();
    httpPostMock = jest.fn();

    httpService = {
      get: httpGetMock,
      post: httpPostMock,
    } as unknown as HttpService;

    appService = {
      getPing: jest.fn(() => ({ status: 'ok', service: 'backend' })),
      getAiServiceUrl: jest.fn(() => 'http://ai_service:8080'),
    } as unknown as AppService;

    firstValueFromSpy = jest.spyOn(rxjs, 'firstValueFrom');
    firstValueFromSpy.mockReset();

    const module: TestingModule = await Test.createTestingModule({
      controllers: [AppController],
      providers: [
        { provide: AppService, useValue: appService },
        { provide: HttpService, useValue: httpService },
      ],
    }).compile();

    appController = module.get<AppController>(AppController);
  });

  afterEach(() => {
    firstValueFromSpy.mockRestore();
  });

  describe('root', () => {
    it('should return a healthy status payload', () => {
      expect(appController.getPing()).toEqual({
        status: 'ok',
        service: 'backend',
      });
    });
  });

  it('proxies the AI health check', async () => {
    const payload = { data: { status: 'ok', service: 'ai_service' } };

    httpGetMock.mockReturnValue('observable placeholder');
    firstValueFromSpy.mockResolvedValue(payload);

    const result = await appController.getAiPing();

    // assert on the mock function, not the object method
    expect(httpGetMock).toHaveBeenCalledWith('http://ai_service:8080/healthz');
    expect(result).toEqual(payload.data);
  });

  it('relays query payloads to the AI service', async () => {
    const payload = { data: { answer: '42' } };

    httpPostMock.mockReturnValue('observable placeholder');
    firstValueFromSpy.mockResolvedValue(payload);

    const result = await appController.queryAi('whois');

    // assert on the mock function, not the object method
    expect(httpPostMock).toHaveBeenCalledWith(
      'http://ai_service:8080/v1/query',
      {
        query: 'whois',
      },
    );
    expect(result).toEqual(payload.data);
  });
});
