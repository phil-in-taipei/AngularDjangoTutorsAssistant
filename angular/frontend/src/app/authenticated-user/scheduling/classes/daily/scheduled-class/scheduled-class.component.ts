import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';

import { 
  ScheduledClassDeletionRequested 
} from '../../../classes-state/scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';


@Component({
  selector: 'app-scheduled-class',
  standalone: false,
  templateUrl: './scheduled-class.component.html',
  styleUrl: './scheduled-class.component.css'
})
export class ScheduledClassComponent {

  @Input() scheduledClass: ScheduledClassModel;

  deletionPopupVisible: boolean = false;

  constructor(private store: Store<ScheduledClassesState>) { }

  showDeletionPopup() {
    this.deletionPopupVisible = true;
  }

  hideDeletionPopup() {
    this.deletionPopupVisible = false;
  }

  onScheduledClassDeletion() {
    const payload = { id: this.scheduledClass.id };
    this.store.dispatch(
      new ScheduledClassDeletionRequested(payload)
    );
  }

}
