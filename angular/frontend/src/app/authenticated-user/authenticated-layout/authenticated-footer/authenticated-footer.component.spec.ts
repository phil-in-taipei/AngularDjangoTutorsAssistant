import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthenticatedFooterComponent } from './authenticated-footer.component';

describe('AuthenticatedFooterComponent', () => {
  let component: AuthenticatedFooterComponent;
  let fixture: ComponentFixture<AuthenticatedFooterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuthenticatedFooterComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AuthenticatedFooterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
