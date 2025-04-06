import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PurchasedHoursModificationRecordsComponent } from './purchased-hours-modification-records.component';

describe('PurchasedHoursModificationRecordsComponent', () => {
  let component: PurchasedHoursModificationRecordsComponent;
  let fixture: ComponentFixture<PurchasedHoursModificationRecordsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PurchasedHoursModificationRecordsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PurchasedHoursModificationRecordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
