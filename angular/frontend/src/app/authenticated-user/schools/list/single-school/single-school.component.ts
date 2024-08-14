import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';

import { SchoolsState } from '../../state/school.reducers';
import { SchoolDeletionRequested } from '../../state/school.actions';
import { SchoolModel } from 'src/app/models/school.model';

@Component({
  selector: 'app-single-school',
  standalone: false,
  templateUrl: './single-school.component.html',
  styleUrl: './single-school.component.css'
})
export class SingleSchoolComponent {

  @Input() school: SchoolModel;

  deletionPopupVisible: boolean = false;


  constructor(private store: Store<SchoolsState>) { }

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
