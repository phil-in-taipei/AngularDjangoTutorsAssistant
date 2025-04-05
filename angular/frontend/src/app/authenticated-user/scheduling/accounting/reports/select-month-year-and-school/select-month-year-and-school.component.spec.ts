import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthYearAndSchoolComponent } from './select-month-year-and-school.component';

describe('SelectMonthYearAndSchoolComponent', () => {
  let component: SelectMonthYearAndSchoolComponent;
  let fixture: ComponentFixture<SelectMonthYearAndSchoolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthYearAndSchoolComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthYearAndSchoolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
