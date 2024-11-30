import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalendarScheduleComponent } from './calendar-schedule.component';

describe('CalendarScheduleComponent', () => {
  let component: CalendarScheduleComponent;
  let fixture: ComponentFixture<CalendarScheduleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CalendarScheduleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CalendarScheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
