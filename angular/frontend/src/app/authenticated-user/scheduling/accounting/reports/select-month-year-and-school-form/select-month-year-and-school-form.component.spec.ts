import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthYearAndSchoolFormComponent } from './select-month-year-and-school-form.component';

describe('SelectMonthYearAndSchoolFormComponent', () => {
  let component: SelectMonthYearAndSchoolFormComponent;
  let fixture: ComponentFixture<SelectMonthYearAndSchoolFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthYearAndSchoolFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthYearAndSchoolFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
