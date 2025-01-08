import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateClassFormComponent } from './create-class-form.component';

describe('CreateClassFormComponent', () => {
  let component: CreateClassFormComponent;
  let fixture: ComponentFixture<CreateClassFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateClassFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateClassFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
