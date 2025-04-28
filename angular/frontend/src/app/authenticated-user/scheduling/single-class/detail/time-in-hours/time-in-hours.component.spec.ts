import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeInHoursComponent } from './time-in-hours.component';

describe('TimeInHoursComponent', () => {
  let component: TimeInHoursComponent;
  let fixture: ComponentFixture<TimeInHoursComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TimeInHoursComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TimeInHoursComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
