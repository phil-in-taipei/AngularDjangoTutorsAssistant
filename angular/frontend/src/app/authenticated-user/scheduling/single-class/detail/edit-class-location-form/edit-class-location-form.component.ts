import { Component, Input, EventEmitter, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { 
  RescheduleClassModel 
} from 'src/app/models/scheduled-class.model';
import { 
  RescheduleClassCancelled, RescheduleClassSubmitted 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  ScheduledClassModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { VenueSpaceModel } from 'src/app/models/venues.model';

@Component({
  selector: 'app-edit-class-location-form',
  standalone: false,
  templateUrl: './edit-class-location-form.component.html',
  styleUrl: './edit-class-location-form.component.css'
})
export class EditClassLocationFormComponent {

  @Input() scheduledClass: ScheduledClassModel;
  @Input() venueSpaces: VenueSpaceModel[];
  @Output() closeFormEvent = new EventEmitter<boolean>();

  constructor(
    private store: Store<ScheduledClassesState>
  ) { }


  onSubmitEditedLocation(form: NgForm) {
    console.log('submit edited location now ...')
    console.log(form.value);
    if (form.invalid) {
      this.store.dispatch(new RescheduleClassCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
      this.closeFormEvent.emit(false);
      return;
    }

    let submissionForm: RescheduleClassModel = {
      id: +this.scheduledClass.id,
      date: this.scheduledClass.date.toString(),
      start_time: this.scheduledClass.start_time.toString(),
      finish_time: this.scheduledClass.finish_time.toString(),
      student_or_class: this.scheduledClass.student_or_class,
      teacher: this.scheduledClass.teacher,
      location: form.value.location ? +form.value.location : null,
    }
    console.log(submissionForm);
    this.store.dispatch(new RescheduleClassSubmitted(
      { id: this.scheduledClass.id, scheduledClass: submissionForm }
    ));    
    form.reset();
    this.closeFormEvent.emit(false);
  }
}
