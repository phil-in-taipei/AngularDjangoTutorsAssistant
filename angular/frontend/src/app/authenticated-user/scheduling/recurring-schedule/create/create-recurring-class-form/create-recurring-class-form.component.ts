import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';
import { NgForm } from '@angular/forms';

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

@Component({
  selector: 'app-create-recurring-class-form',
  standalone: false,
  templateUrl: './create-recurring-class-form.component.html',
  styleUrl: './create-recurring-class-form.component.css'
})
export class CreateRecurringClassFormComponent {

  @Input() studentsOrClasses: StudentOrClassModel[];
  @Input() userProfile: UserProfileModel;
  classDurationOptions: DurationOptionsInterface[];

  constructor(
    private store: Store<RecurringClassesState>
  ) {}

  ngOnit(): void {
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
    let startTimeStr = getFormattedTime(form.value.hour, form.value.minute);
    let durationArr = form.value.duration.split(',')
    let dt = new Date();
    dt.setHours(form.value.hour);
    dt.setMinutes(form.value.minute);
    let finishTimeStr = getFinishTime(dt, durationArr);
    let submissionForm: RecurringClassCreateModel = {
        teacher: this.userProfile.id,
        student_or_class: form.value.student_or_class,
        recurring_day_of_week: +form.value.day_of_week,
        recurring_finish_time: finishTimeStr,
        recurring_start_time: startTimeStr,
    }
    this.store.dispatch(new RecurringClassCreateSubmitted(
        { recurringClass: submissionForm }
      )
    );
    form.resetForm()
  }

}
