import {
  Component, Input, OnChanges, OnInit, SimpleChanges
} from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';
import { NgbTimeStruct } from '@ng-bootstrap/ng-bootstrap';

import { DurationOptionsInterface } from 'src/app/models/time-related.model';
import {
  getClassDurationsOptions, getFinishTime, getFormattedTime
} from 'src/app/shared-utils/date-time.util';
import {
  RecurringClassModel, RecurringClassUpdateModel
} from 'src/app/models/recurring-schedule.model';
import {
  RecurringClassUpdateCancelled, RecurringClassUpdateSubmitted
} from '../../state/recurring-schedule-state/recurring-schedule.actions';
import {
  RecurringClassesState
} from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { VenueSpaceModel } from 'src/app/models/venues.model';

@Component({
  selector: 'app-edit-recurring-class-form',
  standalone: false,
  templateUrl: './edit-recurring-class-form.component.html',
  styleUrl: './edit-recurring-class-form.component.css'
})
export class EditRecurringClassFormComponent implements OnInit, OnChanges {

  @Input() recurringClass: RecurringClassModel;
  @Input() venueSpaces: VenueSpaceModel[];

  classDurationOptions: DurationOptionsInterface[];

  // Form model
  dayOfWeek: number | null = null;
  startTime: NgbTimeStruct = { hour: 13, minute: 0, second: 0 };
  duration: DurationOptionsInterface | null = null;
  location: number | null = null;

  constructor(private store: Store<RecurringClassesState>) {}

  ngOnInit(): void {
    this.classDurationOptions = getClassDurationsOptions();
    this.populateForm();
  }

  ngOnChanges(changes: SimpleChanges): void {
    // The first change is handled in ngOnInit (options must exist first).
    // Later changes happen when the store holds the saved version.
    if (changes['recurringClass'] && !changes['recurringClass'].firstChange) {
      this.populateForm();
    }
  }

  private populateForm(): void {
    const rc = this.recurringClass;
    const [startH, startM] = rc.recurring_start_time.split(':').map(Number);
    const [finishH, finishM] = rc.recurring_finish_time.split(':').map(Number);

    this.dayOfWeek = rc.recurring_day_of_week;
    this.startTime = { hour: startH, minute: startM, second: 0 };
    this.location = rc.recurring_location;

    // Stored finish time is (start + duration - 1 minute), so add the minute back.
    const durationMins =
      (finishH * 60 + finishM) - (startH * 60 + startM) + 1;

    this.duration = this.classDurationOptions.find(
      opt => opt.timeArr[0] * 60 + opt.timeArr[1] === durationMins
    ) ?? null;
  }

  onSubmit(form: NgForm): void {
    if (form.invalid || !this.duration) {
      this.store.dispatch(new RecurringClassUpdateCancelled({
        err: { error: { Error: 'The form values were not properly filled in!' } }
      }));
      return;
    }

    const { hour, minute } = this.startTime;
    const dt = new Date();
    dt.setHours(hour, minute, 0, 0);

    const changes: RecurringClassUpdateModel = {
      recurring_start_time: getFormattedTime(hour, minute),
      recurring_finish_time: getFinishTime(dt, this.duration.timeArr as any),
      recurring_day_of_week: this.dayOfWeek as number,
      recurring_location: this.location !== null ? +this.location : null
    };

    this.store.dispatch(new RecurringClassUpdateSubmitted(
      { id: this.recurringClass.id, changes }
    ));
  }

}
