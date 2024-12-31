import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentOrClassDetailComponent } from './student-or-class-detail.component';

describe('StudentOrClassDetailComponent', () => {
  let component: StudentOrClassDetailComponent;
  let fixture: ComponentFixture<StudentOrClassDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudentOrClassDetailComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StudentOrClassDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
