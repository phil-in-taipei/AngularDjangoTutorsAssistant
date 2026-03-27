import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VenueSpaceTemplateStrComponent } from './venue-space-template-str.component';

describe('VenueSpaceTemplateStrComponent', () => {
  let component: VenueSpaceTemplateStrComponent;
  let fixture: ComponentFixture<VenueSpaceTemplateStrComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VenueSpaceTemplateStrComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(VenueSpaceTemplateStrComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
