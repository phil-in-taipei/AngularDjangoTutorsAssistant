import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentOrClassTemplateStringComponent } from './student-or-class-template-string.component';

describe('StudentOrClassTemplateStringComponent', () => {
  let component: StudentOrClassTemplateStringComponent;
  let fixture: ComponentFixture<StudentOrClassTemplateStringComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudentOrClassTemplateStringComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StudentOrClassTemplateStringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
