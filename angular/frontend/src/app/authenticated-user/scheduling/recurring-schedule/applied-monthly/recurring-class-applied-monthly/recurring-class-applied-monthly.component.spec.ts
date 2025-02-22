import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecurringClassAppliedMonthlyComponent } from './recurring-class-applied-monthly.component';

describe('RecurringClassAppliedMonthlyComponent', () => {
  let component: RecurringClassAppliedMonthlyComponent;
  let fixture: ComponentFixture<RecurringClassAppliedMonthlyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecurringClassAppliedMonthlyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecurringClassAppliedMonthlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
