import { TestBed } from '@angular/core/testing';

import { RecurringScheduleService } from './recurring-schedule.service';

describe('RecurringScheduleService', () => {
  let service: RecurringScheduleService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RecurringScheduleService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
