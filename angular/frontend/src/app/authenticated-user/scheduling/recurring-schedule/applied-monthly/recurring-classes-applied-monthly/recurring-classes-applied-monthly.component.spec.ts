import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecurringClassesAppliedMonthlyComponent } from './recurring-classes-applied-monthly.component';

describe('RecurringClassesAppliedMonthlyComponent', () => {
  let component: RecurringClassesAppliedMonthlyComponent;
  let fixture: ComponentFixture<RecurringClassesAppliedMonthlyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecurringClassesAppliedMonthlyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecurringClassesAppliedMonthlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
