import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecurringClassComponent } from './recurring-class.component';

describe('RecurringClassComponent', () => {
  let component: RecurringClassComponent;
  let fixture: ComponentFixture<RecurringClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecurringClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecurringClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
