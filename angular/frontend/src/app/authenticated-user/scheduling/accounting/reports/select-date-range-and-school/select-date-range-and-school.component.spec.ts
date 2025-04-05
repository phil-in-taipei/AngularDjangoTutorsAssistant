import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectDateRangeAndSchoolComponent } from './select-date-range-and-school.component';

describe('SelectDateRangeAndSchoolComponent', () => {
  let component: SelectDateRangeAndSchoolComponent;
  let fixture: ComponentFixture<SelectDateRangeAndSchoolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectDateRangeAndSchoolComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectDateRangeAndSchoolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
