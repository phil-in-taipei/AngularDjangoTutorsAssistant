import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthYearAndFreelanceAccountComponent } from './select-month-year-and-freelance-account.component';

describe('SelectMonthYearAndFreelanceAccountComponent', () => {
  let component: SelectMonthYearAndFreelanceAccountComponent;
  let fixture: ComponentFixture<SelectMonthYearAndFreelanceAccountComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthYearAndFreelanceAccountComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthYearAndFreelanceAccountComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
