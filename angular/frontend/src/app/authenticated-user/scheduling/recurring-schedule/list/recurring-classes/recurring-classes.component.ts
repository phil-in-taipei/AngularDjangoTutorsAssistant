import { Component, OnInit } from '@angular/core';
import { Observable, of } from "rxjs";
import { select, Store } from '@ngrx/store';

import { 
  RecurringClassDeletionModeActivated, 
  RecurringClassDeletionModeDeactivated 
} from '../../state/recurring-schedule-state/recurring-schedule.actions';
import { 
  RecurringClassesState
 } from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassModel } from 'src/app/models/recurring-schedule.model';
import { 
  deletionModeForRecurringClassesActivated,
  selectAllRecurringClasses, selectRecurringClassesLoaded 
} from '../../state/recurring-schedule-state/recurring-schedule.selectors';

@Component({
  selector: 'app-recurring-classes',
  standalone: false,
  templateUrl: './recurring-classes.component.html',
  styleUrl: './recurring-classes.component.css'
})
export class RecurringClassesComponent implements OnInit {

  deletionModeForRecurringClassesActivated$: Observable<boolean> = of(false);
  recurringClasses$: Observable<RecurringClassModel[] | undefined> = of(undefined);
  recurringClassesLoaded$: Observable<boolean> = of(false);

  constructor(private store: Store<RecurringClassesState>) { }

  ngOnInit(): void {
    this.deletionModeForRecurringClassesActivated$ = this.store.pipe(
      select(deletionModeForRecurringClassesActivated)
    );
    this.recurringClasses$ = this.store.pipe(
      select(selectAllRecurringClasses)
    );
    this.recurringClassesLoaded$ = this.store.pipe(
      select(selectRecurringClassesLoaded)
    );
  }

  onActivateRecurringClassDeletionMode(): void {
    this.store.dispatch(
      new RecurringClassDeletionModeActivated()
    );
  }

  onDeactivateRecurringClassDeletionMode(): void {
    this.store.dispatch(
      new RecurringClassDeletionModeDeactivated()
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }  
}
