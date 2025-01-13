import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditClassStatusFormComponent } from './edit-class-status-form.component';

describe('EditClassStatusFormComponent', () => {
  let component: EditClassStatusFormComponent;
  let fixture: ComponentFixture<EditClassStatusFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditClassStatusFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditClassStatusFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
