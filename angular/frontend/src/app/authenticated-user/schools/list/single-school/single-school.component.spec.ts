import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleSchoolComponent } from './single-school.component';

describe('SingleSchoolComponent', () => {
  let component: SingleSchoolComponent;
  let fixture: ComponentFixture<SingleSchoolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SingleSchoolComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SingleSchoolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
