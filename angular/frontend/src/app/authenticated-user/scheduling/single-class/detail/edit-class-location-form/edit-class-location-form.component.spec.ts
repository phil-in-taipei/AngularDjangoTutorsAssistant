import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditClassLocationFormComponent } from './edit-class-location-form.component';

describe('EditClassLocationFormComponent', () => {
  let component: EditClassLocationFormComponent;
  let fixture: ComponentFixture<EditClassLocationFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditClassLocationFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditClassLocationFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
