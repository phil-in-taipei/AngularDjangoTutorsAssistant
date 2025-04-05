import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverallMonthlyAccountingReportComponent } from './overall-monthly-accounting-report.component';

describe('OverallMonthlyAccountingReportComponent', () => {
  let component: OverallMonthlyAccountingReportComponent;
  let fixture: ComponentFixture<OverallMonthlyAccountingReportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OverallMonthlyAccountingReportComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverallMonthlyAccountingReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
