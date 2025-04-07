import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MakeRefundComponent } from './make-refund.component';

describe('MakeRefundComponent', () => {
  let component: MakeRefundComponent;
  let fixture: ComponentFixture<MakeRefundComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MakeRefundComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MakeRefundComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
