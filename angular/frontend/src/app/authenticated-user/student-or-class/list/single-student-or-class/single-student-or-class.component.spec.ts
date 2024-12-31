import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleStudentOrClassComponent } from './single-student-or-class.component';

describe('SingleStudentOrClassComponent', () => {
  let component: SingleStudentOrClassComponent;
  let fixture: ComponentFixture<SingleStudentOrClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SingleStudentOrClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SingleStudentOrClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
