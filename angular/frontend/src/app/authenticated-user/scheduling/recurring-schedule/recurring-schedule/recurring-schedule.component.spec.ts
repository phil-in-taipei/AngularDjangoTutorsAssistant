import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecurringScheduleComponent } from './recurring-schedule.component';

describe('RecurringScheduleComponent', () => {
  let component: RecurringScheduleComponent;
  let fixture: ComponentFixture<RecurringScheduleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RecurringScheduleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecurringScheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
