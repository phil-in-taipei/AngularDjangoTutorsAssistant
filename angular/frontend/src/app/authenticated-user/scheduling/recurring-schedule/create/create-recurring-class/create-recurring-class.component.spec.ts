import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateRecurringClassComponent } from './create-recurring-class.component';

describe('CreateRecurringClassComponent', () => {
  let component: CreateRecurringClassComponent;
  let fixture: ComponentFixture<CreateRecurringClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateRecurringClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateRecurringClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
