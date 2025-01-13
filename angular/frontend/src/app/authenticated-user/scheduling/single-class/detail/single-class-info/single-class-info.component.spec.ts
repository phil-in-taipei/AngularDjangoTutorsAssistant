import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleClassInfoComponent } from './single-class-info.component';

describe('SingleClassInfoComponent', () => {
  let component: SingleClassInfoComponent;
  let fixture: ComponentFixture<SingleClassInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SingleClassInfoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SingleClassInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
