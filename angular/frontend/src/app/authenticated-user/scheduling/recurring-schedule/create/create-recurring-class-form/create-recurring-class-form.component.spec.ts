import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateRecurringClassFormComponent } from './create-recurring-class-form.component';

describe('CreateRecurringClassFormComponent', () => {
  let component: CreateRecurringClassFormComponent;
  let fixture: ComponentFixture<CreateRecurringClassFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateRecurringClassFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateRecurringClassFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
