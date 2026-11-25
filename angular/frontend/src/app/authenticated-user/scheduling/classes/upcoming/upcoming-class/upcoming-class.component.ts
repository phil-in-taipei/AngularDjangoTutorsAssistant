import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from "rxjs";
import { select, Store } from '@ngrx/store';

import { 
  deletionModeForScheduledClassesActivated 
} from '../../../classes-state/scheduled-classes.selectors';
import { 
  ScheduledClassDeletionRequested 
} from '../../../classes-state/scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';


@Component({
  selector: 'app-upcoming-class',
  standalone: false,
  templateUrl: './upcoming-class.component.html',
  styleUrl: './upcoming-class.component.css'
})
export class UpcomingClassComponent implements OnInit {

  @Input() scheduledClass: ScheduledClassModel;
  deletionModeForScheduledClassesActivated$: Observable<boolean> = of(false);
  deletionPopupVisible: boolean = false;

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.deletionModeForScheduledClassesActivated$ = this.store.pipe(
      select(deletionModeForScheduledClassesActivated)
    );
  }

  showDelPopup() {
    this.deletionPopupVisible = true;
  }

  hideDelPopup() {
    this.deletionPopupVisible = false;
  }

  onFutureClassDeletion() {
    const payload = { id: this.scheduledClass.id };
    this.store.dispatch(
      new ScheduledClassDeletionRequested(payload)
    );
  }

}
