import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MonthlyFreelanceAccountActivityRecordsComponent } from './monthly-freelance-account-activity-records.component';

describe('MonthlyFreelanceAccountActivityRecordsComponent', () => {
  let component: MonthlyFreelanceAccountActivityRecordsComponent;
  let fixture: ComponentFixture<MonthlyFreelanceAccountActivityRecordsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MonthlyFreelanceAccountActivityRecordsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MonthlyFreelanceAccountActivityRecordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
