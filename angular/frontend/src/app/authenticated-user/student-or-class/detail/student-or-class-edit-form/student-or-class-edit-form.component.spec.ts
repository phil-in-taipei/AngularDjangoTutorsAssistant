import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentOrClassEditFormComponent } from './student-or-class-edit-form.component';

describe('StudentOrClassEditFormComponent', () => {
  let component: StudentOrClassEditFormComponent;
  let fixture: ComponentFixture<StudentOrClassEditFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudentOrClassEditFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StudentOrClassEditFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
