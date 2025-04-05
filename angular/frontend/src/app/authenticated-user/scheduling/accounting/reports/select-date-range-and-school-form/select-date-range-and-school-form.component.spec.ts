import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectDateRangeAndSchoolFormComponent } from './select-date-range-and-school-form.component';

describe('SelectDateRangeAndSchoolFormComponent', () => {
  let component: SelectDateRangeAndSchoolFormComponent;
  let fixture: ComponentFixture<SelectDateRangeAndSchoolFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectDateRangeAndSchoolFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectDateRangeAndSchoolFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
