import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScheduleSingleClassComponent } from './schedule-single-class.component';

describe('ScheduleSingleClassComponent', () => {
  let component: ScheduleSingleClassComponent;
  let fixture: ComponentFixture<ScheduleSingleClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScheduleSingleClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ScheduleSingleClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
