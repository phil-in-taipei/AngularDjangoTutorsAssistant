import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MakeRefundFormComponent } from './make-refund-form.component';

describe('MakeRefundFormComponent', () => {
  let component: MakeRefundFormComponent;
  let fixture: ComponentFixture<MakeRefundFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MakeRefundFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MakeRefundFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
