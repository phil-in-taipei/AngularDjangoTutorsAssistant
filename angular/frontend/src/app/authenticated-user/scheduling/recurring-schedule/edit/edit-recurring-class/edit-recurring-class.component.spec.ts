import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditRecurringClassComponent } from './edit-recurring-class.component';

describe('EditRecurringClassComponent', () => {
  let component: EditRecurringClassComponent;
  let fixture: ComponentFixture<EditRecurringClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditRecurringClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditRecurringClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
