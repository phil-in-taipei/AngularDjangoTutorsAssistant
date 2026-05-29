import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupClassAttendanceEditFormComponent } from './group-class-attendance-edit-form.component';

describe('GroupClassAttendanceEditFormComponent', () => {
  let component: GroupClassAttendanceEditFormComponent;
  let fixture: ComponentFixture<GroupClassAttendanceEditFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GroupClassAttendanceEditFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GroupClassAttendanceEditFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
