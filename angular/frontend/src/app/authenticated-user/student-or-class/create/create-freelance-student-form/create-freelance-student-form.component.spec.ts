import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateFreelanceStudentFormComponent } from './create-freelance-student-form.component';

describe('CreateFreelanceStudentFormComponent', () => {
  let component: CreateFreelanceStudentFormComponent;
  let fixture: ComponentFixture<CreateFreelanceStudentFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateFreelanceStudentFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateFreelanceStudentFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
