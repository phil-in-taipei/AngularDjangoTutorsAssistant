import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditClassStatusResponseComponent } from './edit-class-status-response.component';

describe('EditClassStatusResponseComponent', () => {
  let component: EditClassStatusResponseComponent;
  let fixture: ComponentFixture<EditClassStatusResponseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditClassStatusResponseComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditClassStatusResponseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
