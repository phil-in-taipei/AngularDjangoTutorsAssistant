import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MakePurchaseFormComponent } from './make-purchase-form.component';

describe('MakePurchaseFormComponent', () => {
  let component: MakePurchaseFormComponent;
  let fixture: ComponentFixture<MakePurchaseFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MakePurchaseFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MakePurchaseFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
