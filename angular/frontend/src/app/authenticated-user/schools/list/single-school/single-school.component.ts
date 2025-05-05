import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { 
  deletionModeActivated
} from '../../state/school.selectors';
import { SchoolsState } from '../../state/school.reducers';
import { SchoolDeletionRequested } from '../../state/school.actions';
import { SchoolModel } from 'src/app/models/school.model';

@Component({
  selector: 'app-single-school',
  standalone: false,
  templateUrl: './single-school.component.html',
  styleUrl: './single-school.component.css'
})
export class SingleSchoolComponent implements OnInit {

  @Input() school: SchoolModel;

  deletionPopupVisible: boolean = false;
  deletionModeActivated$: Observable<boolean> = of(false);

  constructor(private store: Store<SchoolsState>) { }

  ngOnInit(): void {
    this.deletionModeActivated$ = this.store.pipe(
      select(deletionModeActivated)
    );
  }

  showDeletionPopup() {
    this.deletionPopupVisible = true;
  }

  hideDeletionPopup() {
    this.deletionPopupVisible = false;
  }

  onRemoveSchool() {
    const payload = { id: +this.school.id };
    this.store.dispatch(
      new SchoolDeletionRequested(payload)
    );
  }

}
