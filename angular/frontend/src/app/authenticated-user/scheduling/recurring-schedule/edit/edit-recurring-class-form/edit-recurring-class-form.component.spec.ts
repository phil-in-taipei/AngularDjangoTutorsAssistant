import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditRecurringClassFormComponent } from './edit-recurring-class-form.component';

describe('EditRecurringClassFormComponent', () => {
  let component: EditRecurringClassFormComponent;
  let fixture: ComponentFixture<EditRecurringClassFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditRecurringClassFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditRecurringClassFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
