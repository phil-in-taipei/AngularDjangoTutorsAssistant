import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupClassAttendanceDetailComponent } from './group-class-attendance-detail.component';

describe('GroupClassAttendanceDetailComponent', () => {
  let component: GroupClassAttendanceDetailComponent;
  let fixture: ComponentFixture<GroupClassAttendanceDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GroupClassAttendanceDetailComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GroupClassAttendanceDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
