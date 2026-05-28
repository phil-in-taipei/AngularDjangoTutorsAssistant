import { TestBed } from '@angular/core/testing';

import { GroupClassAttendanceService } from './group-class-attendance.service';

describe('GroupClassAttendanceService', () => {
  let service: GroupClassAttendanceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GroupClassAttendanceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
