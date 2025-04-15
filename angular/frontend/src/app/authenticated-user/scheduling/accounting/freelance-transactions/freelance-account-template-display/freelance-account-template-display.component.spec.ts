import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FreelanceAccountTemplateDisplayComponent } from './freelance-account-template-display.component';

describe('FreelanceAccountTemplateDisplayComponent', () => {
  let component: FreelanceAccountTemplateDisplayComponent;
  let fixture: ComponentFixture<FreelanceAccountTemplateDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FreelanceAccountTemplateDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FreelanceAccountTemplateDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
