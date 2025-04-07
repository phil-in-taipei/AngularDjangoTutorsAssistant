import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostRefundHoursUpdateComponent } from './post-refund-hours-update.component';

describe('PostRefundHoursUpdateComponent', () => {
  let component: PostRefundHoursUpdateComponent;
  let fixture: ComponentFixture<PostRefundHoursUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostRefundHoursUpdateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PostRefundHoursUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
