import { Component, Input, EventEmitter, OnInit, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { NgbDateStruct, NgbTimeStruct } from '@ng-bootstrap/ng-bootstrap';
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

  dateModel: NgbDateStruct | null = null;
  startTime: NgbTimeStruct = { hour: 13, minute: 0, second: 0 };
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
    const { hour, minute } = form.value.startTime;
    const d = form.value.date;
    const startTimeStr = getFormattedTime(hour, minute);
    const durationArr = form.value.duration.split(',');

    const dt = new Date();
    dt.setHours(hour, minute, 0, 0);
    const finishTimeStr = getFinishTime(dt, durationArr);

    const submissionForm: RescheduleClassModel = {
      id: this.scheduledClass.id,
      student_or_class: this.scheduledClass.student_or_class,
      teacher: this.scheduledClass.teacher,
      date: `${d.year}-${String(d.month).padStart(2, '0')}-${String(d.day).padStart(2, '0')}`,
      start_time: startTimeStr,
      finish_time: finishTimeStr,
      location: this.scheduledClass.location
    };

    this.store.dispatch(new RescheduleClassSubmitted(
      { id: this.scheduledClass.id, scheduledClass: submissionForm }
    ));
    form.resetForm();
    this.closeFormEvent.emit(false);
  }

}
