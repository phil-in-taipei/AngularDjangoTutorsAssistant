import { TestBed } from '@angular/core/testing';

import { VenuesServiceService } from './venues-service.service';

describe('VenuesServiceService', () => {
  let service: VenuesServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VenuesServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
