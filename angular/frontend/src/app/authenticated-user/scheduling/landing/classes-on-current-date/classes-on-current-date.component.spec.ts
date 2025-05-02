import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassesOnCurrentDateComponent } from './classes-on-current-date.component';

describe('ClassesOnCurrentDateComponent', () => {
  let component: ClassesOnCurrentDateComponent;
  let fixture: ComponentFixture<ClassesOnCurrentDateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassesOnCurrentDateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClassesOnCurrentDateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
