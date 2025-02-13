import { Component, OnInit } from '@angular/core';
import { Observable, of } from "rxjs";
import { select, Store } from '@ngrx/store';

import { 
  RecurringClassesState
 } from '../../recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassModel } from 'src/app/models/recurring-schedule.model';
import { 
  selectAllRecurringClasses, selectRecurringClassesLoaded 
} from '../../recurring-schedule-state/recurring-schedule.selectors';

@Component({
  selector: 'app-recurring-classes',
  standalone: false,
  templateUrl: './recurring-classes.component.html',
  styleUrl: './recurring-classes.component.css'
})
export class RecurringClassesComponent {

  recurringClasses$: Observable<RecurringClassModel[] | undefined> = of(undefined);
  recurringClassesLoaded$: Observable<boolean> = of(false);

  constructor(private store: Store<RecurringClassesState>) { }

  ngOnInit(): void {
    this.recurringClasses$ = this.store.pipe(
      select(selectAllRecurringClasses)
    );
    this.recurringClassesLoaded$ = this.store.pipe(
      select(selectRecurringClassesLoaded)
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }  
}
