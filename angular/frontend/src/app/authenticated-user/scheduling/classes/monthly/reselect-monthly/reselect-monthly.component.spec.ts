import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReselectMonthlyComponent } from './reselect-monthly.component';

describe('ReselectMonthlyComponent', () => {
  let component: ReselectMonthlyComponent;
  let fixture: ComponentFixture<ReselectMonthlyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReselectMonthlyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ReselectMonthlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
