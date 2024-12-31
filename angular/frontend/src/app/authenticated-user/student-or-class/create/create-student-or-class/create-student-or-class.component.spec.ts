import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateStudentOrClassComponent } from './create-student-or-class.component';

describe('CreateStudentOrClassComponent', () => {
  let component: CreateStudentOrClassComponent;
  let fixture: ComponentFixture<CreateStudentOrClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateStudentOrClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateStudentOrClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
