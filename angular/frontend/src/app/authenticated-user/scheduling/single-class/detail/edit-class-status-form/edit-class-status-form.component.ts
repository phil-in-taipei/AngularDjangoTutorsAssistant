import { Component, Input, EventEmitter, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { 
  ModifyClassStatusModel, ScheduledClassModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  ClassStatusUpdateCancelled,  ClassStatusUpdateSubmitted
 } from '../../../classes-state/scheduled-classes.actions';

@Component({
  selector: 'app-edit-class-status-form',
  standalone: false,
  templateUrl: './edit-class-status-form.component.html',
  styleUrl: './edit-class-status-form.component.css'
})
export class EditClassStatusFormComponent {
  
  @Input() scheduledClass: ScheduledClassModel;
  @Output() closeFormEvent = new EventEmitter<boolean>();

  constructor(
    private store: Store<ScheduledClassesState>
  ) { }


  onSubmitClassStatusUpdate(form: NgForm) {

    if (form.invalid) {
      //console.log('the form is invalid!')
      this.store.dispatch(new ClassStatusUpdateCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
      this.closeFormEvent.emit(false);
      return;
    }

    let submissionForm: ModifyClassStatusModel = {
      id: this.scheduledClass.id,
      class_status: form.value.class_status,
      teacher_notes: form.value.teacher_notes,
      class_content: form.value.class_content
    }
    this.store.dispatch(new ClassStatusUpdateSubmitted(
      { scheduledClass: submissionForm }
    ));
    form.resetForm();
    this.closeFormEvent.emit(false);
  }

}
