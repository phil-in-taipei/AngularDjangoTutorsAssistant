import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnconfirmedClassesComponent } from './unconfirmed-classes.component';

describe('UnconfirmedClassesComponent', () => {
  let component: UnconfirmedClassesComponent;
  let fixture: ComponentFixture<UnconfirmedClassesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnconfirmedClassesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UnconfirmedClassesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
