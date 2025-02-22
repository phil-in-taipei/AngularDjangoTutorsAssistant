import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplyRecurringClassMonthlyFormComponent } from './apply-recurring-class-monthly-form.component';

describe('ApplyRecurringClassMonthlyFormComponent', () => {
  let component: ApplyRecurringClassMonthlyFormComponent;
  let fixture: ComponentFixture<ApplyRecurringClassMonthlyFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApplyRecurringClassMonthlyFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ApplyRecurringClassMonthlyFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
