import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScheduleSingleClassFormComponent } from './schedule-single-class-form.component';

describe('ScheduleSingleClassFormComponent', () => {
  let component: ScheduleSingleClassFormComponent;
  let fixture: ComponentFixture<ScheduleSingleClassFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScheduleSingleClassFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ScheduleSingleClassFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
