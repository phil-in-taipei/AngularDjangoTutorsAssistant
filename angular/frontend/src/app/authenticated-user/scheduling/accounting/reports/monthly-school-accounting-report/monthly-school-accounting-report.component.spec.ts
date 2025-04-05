import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MonthlySchoolAccountingReportComponent } from './monthly-school-accounting-report.component';

describe('MonthlySchoolAccountingReportComponent', () => {
  let component: MonthlySchoolAccountingReportComponent;
  let fixture: ComponentFixture<MonthlySchoolAccountingReportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MonthlySchoolAccountingReportComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MonthlySchoolAccountingReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
