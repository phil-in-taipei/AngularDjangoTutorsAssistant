import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FreelancePaymentsAndRefundsComponent } from './freelance-payments-and-refunds.component';

describe('FreelancePaymentsAndRefundsComponent', () => {
  let component: FreelancePaymentsAndRefundsComponent;
  let fixture: ComponentFixture<FreelancePaymentsAndRefundsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FreelancePaymentsAndRefundsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FreelancePaymentsAndRefundsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
