import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClientSchoolAccountingMsgComponent } from './client-school-accounting-msg.component';

describe('ClientSchoolAccountingMsgComponent', () => {
  let component: ClientSchoolAccountingMsgComponent;
  let fixture: ComponentFixture<ClientSchoolAccountingMsgComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClientSchoolAccountingMsgComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClientSchoolAccountingMsgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
