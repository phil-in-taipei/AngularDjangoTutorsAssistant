import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectMonthlyComponent } from './select-monthly.component';

describe('SelectMonthlyComponent', () => {
  let component: SelectMonthlyComponent;
  let fixture: ComponentFixture<SelectMonthlyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectMonthlyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SelectMonthlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
