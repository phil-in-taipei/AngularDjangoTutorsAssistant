import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VenueSpaceTemplateStringComponent } from './venue-space-template-string.component';

describe('VenueSpaceTemplateStringComponent', () => {
  let component: VenueSpaceTemplateStringComponent;
  let fixture: ComponentFixture<VenueSpaceTemplateStringComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VenueSpaceTemplateStringComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(VenueSpaceTemplateStringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
