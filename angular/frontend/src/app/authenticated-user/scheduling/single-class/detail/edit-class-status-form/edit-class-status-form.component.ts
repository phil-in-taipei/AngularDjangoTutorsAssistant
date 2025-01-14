import { Component, Input, EventEmitter, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { 
  ModifyClassStatusModel, ScheduledClassModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';

@Component({
  selector: 'app-edit-class-status-form',
  standalone: false,
  templateUrl: './edit-class-status-form.component.html',
  styleUrl: './edit-class-status-form.component.css'
})
export class EditClassStatusFormComponent {
  
  @Input() scheduledClass: ScheduledClassModel;
  @Output() closeFormEvent = new EventEmitter<boolean>();

  constructor(private store: Store<ScheduledClassesState>) { }
}
