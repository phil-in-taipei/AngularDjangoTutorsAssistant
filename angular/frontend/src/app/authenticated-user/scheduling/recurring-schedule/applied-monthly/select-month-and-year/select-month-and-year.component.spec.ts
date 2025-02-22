import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthAndYearComponent } from './select-month-and-year.component';

describe('SelectMonthAndYearComponent', () => {
  let component: SelectMonthAndYearComponent;
  let fixture: ComponentFixture<SelectMonthAndYearComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthAndYearComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthAndYearComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
