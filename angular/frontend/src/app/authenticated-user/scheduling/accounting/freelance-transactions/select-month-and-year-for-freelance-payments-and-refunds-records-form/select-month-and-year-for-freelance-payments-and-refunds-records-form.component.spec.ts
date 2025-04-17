import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent } from './select-month-and-year-for-freelance-payments-and-refunds-records-form.component';

describe('SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent', () => {
  let component: SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent;
  let fixture: ComponentFixture<SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
