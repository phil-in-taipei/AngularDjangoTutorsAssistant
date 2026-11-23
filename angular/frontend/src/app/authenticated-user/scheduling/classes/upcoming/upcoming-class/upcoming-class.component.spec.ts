import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpcomingClassComponent } from './upcoming-class.component';

describe('UpcomingClassComponent', () => {
  let component: UpcomingClassComponent;
  let fixture: ComponentFixture<UpcomingClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpcomingClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UpcomingClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
