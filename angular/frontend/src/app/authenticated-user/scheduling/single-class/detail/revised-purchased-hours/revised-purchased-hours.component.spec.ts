import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RevisedPurchasedHoursComponent } from './revised-purchased-hours.component';

describe('RevisedPurchasedHoursComponent', () => {
  let component: RevisedPurchasedHoursComponent;
  let fixture: ComponentFixture<RevisedPurchasedHoursComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RevisedPurchasedHoursComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RevisedPurchasedHoursComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
