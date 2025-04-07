import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RefundResponseDisplayComponent } from './refund-response-display.component';

describe('RefundResponseDisplayComponent', () => {
  let component: RefundResponseDisplayComponent;
  let fixture: ComponentFixture<RefundResponseDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RefundResponseDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RefundResponseDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
