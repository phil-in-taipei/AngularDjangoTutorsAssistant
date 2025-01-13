import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RescheduleClassFormComponent } from './reschedule-class-form.component';

describe('RescheduleClassFormComponent', () => {
  let component: RescheduleClassFormComponent;
  let fixture: ComponentFixture<RescheduleClassFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RescheduleClassFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RescheduleClassFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
