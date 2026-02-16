import { Module } from '@nestjs/common/decorators/modules/module.decorator';
import { AiController } from './ai.controller';
import { AiService } from './ai.service';


@Module({
  controllers: [AiController],
  providers: [AiService],
})
export class AiModule {}