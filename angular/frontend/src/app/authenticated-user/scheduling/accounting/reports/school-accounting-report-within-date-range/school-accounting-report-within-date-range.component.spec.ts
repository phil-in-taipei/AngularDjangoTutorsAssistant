import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchoolAccountingReportWithinDateRangeComponent } from './school-accounting-report-within-date-range.component';

describe('SchoolAccountingReportWithinDateRangeComponent', () => {
  let component: SchoolAccountingReportWithinDateRangeComponent;
  let fixture: ComponentFixture<SchoolAccountingReportWithinDateRangeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SchoolAccountingReportWithinDateRangeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SchoolAccountingReportWithinDateRangeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
