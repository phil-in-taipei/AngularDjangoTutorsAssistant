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
  selector: 'app-scheduled-class',
  standalone: false,
  templateUrl: './scheduled-class.component.html',
  styleUrl: './scheduled-class.component.css'
})
export class ScheduledClassComponent implements OnInit {

  @Input() scheduledClass: ScheduledClassModel;
  deletionModeForScheduledClassesActivated$: Observable<boolean> = of(false);
  deletionPopupVisible: boolean = false;

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.deletionModeForScheduledClassesActivated$ = this.store.pipe(
      select(deletionModeForScheduledClassesActivated)
    );
  }

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
