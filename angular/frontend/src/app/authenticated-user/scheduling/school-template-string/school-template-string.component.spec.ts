import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchoolTemplateStringComponent } from './school-template-string.component';

describe('SchoolTemplateStringComponent', () => {
  let component: SchoolTemplateStringComponent;
  let fixture: ComponentFixture<SchoolTemplateStringComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SchoolTemplateStringComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SchoolTemplateStringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
