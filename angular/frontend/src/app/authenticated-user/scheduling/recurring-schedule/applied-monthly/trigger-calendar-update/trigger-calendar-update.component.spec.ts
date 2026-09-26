import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TriggerCalendarUpdateComponent } from './trigger-calendar-update.component';

describe('TriggerCalendarUpdateComponent', () => {
  let component: TriggerCalendarUpdateComponent;
  let fixture: ComponentFixture<TriggerCalendarUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TriggerCalendarUpdateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TriggerCalendarUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
