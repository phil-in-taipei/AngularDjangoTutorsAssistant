import { Component, OnInit, Input } from '@angular/core';
import { NgForm, NgModel } from '@angular/forms';
import { Store } from '@ngrx/store';

import { CreateScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { DurationOptionsInterface } from 'src/app/models/time-related.model';
import { 
  getClassDurationsOptions, getFinishTime, getFormattedTime 
} from 'src/app/shared-utils/date-time.util';
import { 
  ScheduleSingleClassCancelled, ScheduleSingleClassSubmitted 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { UserProfileModel } from 'src/app/models/user-profile.model';

@Component({
  selector: 'app-schedule-single-class-form',
  standalone: false,
  templateUrl: './schedule-single-class-form.component.html',
  styleUrl: './schedule-single-class-form.component.css'
})
export class ScheduleSingleClassFormComponent implements OnInit{

  @Input() studentsOrClasses: StudentOrClassModel[];
  @Input() userProfile: UserProfileModel;
  dateModel: Date;
  classDurationOptions: DurationOptionsInterface[];

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.classDurationOptions = getClassDurationsOptions();
  }

  onSubmitClass(form: NgForm) {
    if (form.invalid) {
      this.store.dispatch(new ScheduleSingleClassCancelled({err: {
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
    let submissionForm: CreateScheduledClassModel = {
      student_or_class: form.value.student_or_class,
      teacher: this.userProfile.id,
      date: `${form.value.date.year}-${form.value.date.month}-${form.value.date.day}`,
      start_time: startTimeStr,
      finish_time: finishTimeStr,
    }
    this.store.dispatch(new ScheduleSingleClassSubmitted(
        { scheduledClass: submissionForm }
      )
    );
    form.resetForm()
  }  
}
