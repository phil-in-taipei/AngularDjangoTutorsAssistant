import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PurchaseResponseDisplayComponent } from './purchase-response-display.component';

describe('PurchaseResponseDisplayComponent', () => {
  let component: PurchaseResponseDisplayComponent;
  let fixture: ComponentFixture<PurchaseResponseDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PurchaseResponseDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PurchaseResponseDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
