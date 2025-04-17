import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsComponent } from './select-month-and-year-for-freelance-payments-and-refunds-records.component';

describe('SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsComponent', () => {
  let component: SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsComponent;
  let fixture: ComponentFixture<SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
