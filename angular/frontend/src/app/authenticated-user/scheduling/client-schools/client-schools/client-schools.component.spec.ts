import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClientSchoolsComponent } from './client-schools.component';

describe('ClientSchoolsComponent', () => {
  let component: ClientSchoolsComponent;
  let fixture: ComponentFixture<ClientSchoolsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClientSchoolsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClientSchoolsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
