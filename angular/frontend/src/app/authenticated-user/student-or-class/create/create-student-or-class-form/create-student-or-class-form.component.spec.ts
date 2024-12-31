import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateStudentOrClassFormComponent } from './create-student-or-class-form.component';

describe('CreateStudentOrClassFormComponent', () => {
  let component: CreateStudentOrClassFormComponent;
  let fixture: ComponentFixture<CreateStudentOrClassFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateStudentOrClassFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateStudentOrClassFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
