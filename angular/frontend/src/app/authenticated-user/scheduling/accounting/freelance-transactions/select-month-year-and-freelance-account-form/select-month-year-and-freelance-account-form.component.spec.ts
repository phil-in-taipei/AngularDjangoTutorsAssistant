import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthYearAndFreelanceAccountFormComponent } from './select-month-year-and-freelance-account-form.component';

describe('SelectMonthYearAndFreelanceAccountFormComponent', () => {
  let component: SelectMonthYearAndFreelanceAccountFormComponent;
  let fixture: ComponentFixture<SelectMonthYearAndFreelanceAccountFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthYearAndFreelanceAccountFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthYearAndFreelanceAccountFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
