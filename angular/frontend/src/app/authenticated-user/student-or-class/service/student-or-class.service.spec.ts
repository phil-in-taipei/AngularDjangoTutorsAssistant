import { TestBed } from '@angular/core/testing';

import { StudentOrClassService } from './student-or-class.service';

describe('StudentOrClassService', () => {
  let service: StudentOrClassService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StudentOrClassService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
