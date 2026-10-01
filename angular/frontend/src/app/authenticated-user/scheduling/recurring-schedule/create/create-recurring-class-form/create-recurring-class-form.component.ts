import { Component, Input, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { NgForm } from '@angular/forms';
import { NgbTimeStruct } from '@ng-bootstrap/ng-bootstrap';

import { DurationOptionsInterface } from 'src/app/models/time-related.model';
import { 
  getClassDurationsOptions, getFinishTime, getFormattedTime 
} from 'src/app/shared-utils/date-time.util';
import { 
  RecurringClassCreateModel 
} from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassCreateSubmitted, RecurringClassCreationCancelled 
} from '../../state/recurring-schedule-state/recurring-schedule.actions';
import { 
  RecurringClassesState 
} from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { UserProfileModel } from 'src/app/models/user-profile.model';
import { VenueSpaceModel } from 'src/app/models/venues.model';


@Component({
  selector: 'app-create-recurring-class-form',
  standalone: false,
  templateUrl: './create-recurring-class-form.component.html',
  styleUrl: './create-recurring-class-form.component.css'
})
export class CreateRecurringClassFormComponent implements OnInit {

  @Input() studentsOrClasses: StudentOrClassModel[];
  @Input() userProfile: UserProfileModel;
  @Input() venueSpaces: VenueSpaceModel[];
  classDurationOptions: DurationOptionsInterface[];
  startTime: NgbTimeStruct = { hour: 13, minute: 0, second: 0 };

  constructor(
    private store: Store<RecurringClassesState>
  ) {}

  ngOnInit(): void {
    this.classDurationOptions = getClassDurationsOptions();
  }

  onSubmitRecurringClass(form: NgForm) {
    if (form.invalid) {
      this.store.dispatch(new RecurringClassCreationCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
      return;
    }
    const { hour, minute } = form.value.startTime;
    const startTimeStr = getFormattedTime(hour, minute);
    const durationArr = form.value.duration.split(',');

    const dt = new Date();
    dt.setHours(hour, minute, 0, 0);
    const finishTimeStr = getFinishTime(dt, durationArr);

    const submissionForm: RecurringClassCreateModel = {
      teacher: this.userProfile.id,
      student_or_class: form.value.student_or_class,
      recurring_day_of_week: +form.value.day_of_week,
      recurring_finish_time: finishTimeStr,
      recurring_start_time: startTimeStr,
      recurring_location: form.value.recurring_location ? +form.value.recurring_location : null,
    };

    this.store.dispatch(new RecurringClassCreateSubmitted(
      { recurringClass: submissionForm }
    ));
    form.resetForm({ startTime: { hour: 13, minute: 0, second: 0 } });
  }

}
