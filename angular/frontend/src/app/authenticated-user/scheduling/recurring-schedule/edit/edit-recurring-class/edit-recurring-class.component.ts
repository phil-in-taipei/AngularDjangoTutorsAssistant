import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import {
  RecurringClassesMessagesCleared, RecurringClassesRequested
} from '../../state/recurring-schedule-state/recurring-schedule.actions';
import {
  RecurringClassesState
} from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import {
  recurringClassErrorMsg, recurringClassSuccessMsg,
  selectRecurringClassById
} from '../../state/recurring-schedule-state/recurring-schedule.selectors';
import { RecurringClassModel } from 'src/app/models/recurring-schedule.model';
import { selectAllVenueSpaces } from '../../../venues/state/venues.selectors';
import { VenuesSpacesState } from '../../../venues/state/venues.reducers';
import { VenueSpaceModel } from 'src/app/models/venues.model';

@Component({
  selector: 'app-edit-recurring-class',
  standalone: false,
  templateUrl: './edit-recurring-class.component.html',
  styleUrl: './edit-recurring-class.component.css'
})
export class EditRecurringClassComponent implements OnInit {

  errorMessage$: Observable<string | undefined> = of(undefined);
  successMessage$: Observable<string | undefined> = of(undefined);
  recurringClass$: Observable<RecurringClassModel | undefined> = of(undefined);
  venueSpaces$: Observable<VenueSpaceModel[] | undefined> = of(undefined);

  constructor(
    private route: ActivatedRoute,
    private recurringClassesStore: Store<RecurringClassesState>,
    private venuesStore: Store<VenuesSpacesState>
  ) {}

  ngOnInit(): void {
    this.recurringClassesStore.dispatch(new RecurringClassesMessagesCleared());
    // Covers a hard refresh on the edit URL; the effect skips the fetch if
    // the classes are already loaded.
    this.recurringClassesStore.dispatch(new RecurringClassesRequested());

    this.errorMessage$ = this.recurringClassesStore.pipe(
      select(recurringClassErrorMsg)
    );
    this.successMessage$ = this.recurringClassesStore.pipe(
      select(recurringClassSuccessMsg)
    );
    this.venueSpaces$ = this.venuesStore.pipe(select(selectAllVenueSpaces));

    this.recurringClass$ = this.route.paramMap.pipe(
      switchMap(params =>
        this.recurringClassesStore.pipe(
          select(selectRecurringClassById(Number(params.get('id'))))
        )
      )
    );
  }

  onClearStatusMsgs(): void {
    this.recurringClassesStore.dispatch(new RecurringClassesMessagesCleared());
  }

}
