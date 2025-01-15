import { Component, Input, EventEmitter, OnInit, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { DurationOptionsInterface } from 'src/app/models/time-related.model';
import { 
  getClassDurationsOptions, getFinishTime, getFormattedTime 
} from 'src/app/shared-utils/date-time.util';
import { 
  RescheduleClassModel, ScheduledClassModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  RescheduleClassCancelled, RescheduleClassSubmitted 
} from '../../../classes-state/scheduled-classes.actions';

@Component({
  selector: 'app-reschedule-class-form',
  standalone: false,
  templateUrl: './reschedule-class-form.component.html',
  styleUrl: './reschedule-class-form.component.css'
})
export class RescheduleClassFormComponent implements OnInit{

  dateModel: Date;
  @Input() scheduledClass: ScheduledClassModel;
  @Output() closeFormEvent = new EventEmitter<boolean>();
  classDurationOptions: DurationOptionsInterface[];

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.classDurationOptions = getClassDurationsOptions();
  }

  onSubmitRescheduledClass(form: NgForm) {

    if (form.invalid) {
      //console.log('the form is invalid!')
      this.store.dispatch(new RescheduleClassCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
      this.closeFormEvent.emit(false);
      return;
    }
    let startTimeStr = getFormattedTime(form.value.hour, form.value.minute);
    let durationArr = form.value.duration.split(',')
    let dt = new Date();
    dt.setHours(form.value.hour);
    dt.setMinutes(form.value.minute);
    let finishTimeStr = getFinishTime(dt, durationArr);
    let submissionForm: RescheduleClassModel = {
      id: this.scheduledClass.id,
      student_or_class: this.scheduledClass.student_or_class,
      teacher: this.scheduledClass.teacher,
      date: `${form.value.date.year}-${form.value.date.month}-${form.value.date.day}`,
      start_time: startTimeStr,
      finish_time: finishTimeStr,
    }
    this.store.dispatch(new RescheduleClassSubmitted(
      { id: this.scheduledClass.id, scheduledClass: submissionForm }
    ));
    form.resetForm();
    this.closeFormEvent.emit(false);
  }

}
