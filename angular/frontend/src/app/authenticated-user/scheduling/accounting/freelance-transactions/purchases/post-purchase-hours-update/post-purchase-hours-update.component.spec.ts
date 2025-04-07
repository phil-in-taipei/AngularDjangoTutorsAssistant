import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostPurchaseHoursUpdateComponent } from './post-purchase-hours-update.component';

describe('PostPurchaseHoursUpdateComponent', () => {
  let component: PostPurchaseHoursUpdateComponent;
  let fixture: ComponentFixture<PostPurchaseHoursUpdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostPurchaseHoursUpdateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PostPurchaseHoursUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
