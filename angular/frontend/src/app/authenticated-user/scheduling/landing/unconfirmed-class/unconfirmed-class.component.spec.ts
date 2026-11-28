import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnconfirmedClassComponent } from './unconfirmed-class.component';

describe('UnconfirmedClassComponent', () => {
  let component: UnconfirmedClassComponent;
  let fixture: ComponentFixture<UnconfirmedClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnconfirmedClassComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UnconfirmedClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
