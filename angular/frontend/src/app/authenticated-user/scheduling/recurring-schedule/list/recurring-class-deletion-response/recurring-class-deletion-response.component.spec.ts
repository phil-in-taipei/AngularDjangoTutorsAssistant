import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecurringClassDeletionResponseComponent } from './recurring-class-deletion-response.component';

describe('RecurringClassDeletionResponseComponent', () => {
  let component: RecurringClassDeletionResponseComponent;
  let fixture: ComponentFixture<RecurringClassDeletionResponseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecurringClassDeletionResponseComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecurringClassDeletionResponseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
