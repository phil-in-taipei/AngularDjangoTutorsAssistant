import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MakePurchaseComponent } from './make-purchase.component';

describe('MakePurchaseComponent', () => {
  let component: MakePurchaseComponent;
  let fixture: ComponentFixture<MakePurchaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MakePurchaseComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MakePurchaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
