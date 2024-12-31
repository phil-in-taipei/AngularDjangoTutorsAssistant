import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentOrClassListComponent } from './student-or-class-list.component';

describe('StudentOrClassListComponent', () => {
  let component: StudentOrClassListComponent;
  let fixture: ComponentFixture<StudentOrClassListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudentOrClassListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StudentOrClassListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
