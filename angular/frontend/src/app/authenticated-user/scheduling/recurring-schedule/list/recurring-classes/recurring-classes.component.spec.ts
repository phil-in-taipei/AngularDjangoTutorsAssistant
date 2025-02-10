import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecurringClassesComponent } from './recurring-classes.component';

describe('RecurringClassesComponent', () => {
  let component: RecurringClassesComponent;
  let fixture: ComponentFixture<RecurringClassesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecurringClassesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RecurringClassesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
