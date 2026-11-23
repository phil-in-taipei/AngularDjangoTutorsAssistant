import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpcomingClassesByStudentComponent } from './upcoming-classes-by-student.component';

describe('UpcomingClassesByStudentComponent', () => {
  let component: UpcomingClassesByStudentComponent;
  let fixture: ComponentFixture<UpcomingClassesByStudentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpcomingClassesByStudentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UpcomingClassesByStudentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
