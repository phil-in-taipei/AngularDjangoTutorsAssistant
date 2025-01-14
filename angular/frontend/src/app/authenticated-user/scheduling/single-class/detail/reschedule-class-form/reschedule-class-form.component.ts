import { Component, Input, EventEmitter, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { 
  RescheduleClassModel, ScheduledClassModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';

@Component({
  selector: 'app-reschedule-class-form',
  standalone: false,
  templateUrl: './reschedule-class-form.component.html',
  styleUrl: './reschedule-class-form.component.css'
})
export class RescheduleClassFormComponent {

  dateModel: Date;
  @Input() scheduledClass: ScheduledClassModel;
  @Output() closeFormEvent = new EventEmitter<boolean>();

  constructor(private store: Store<ScheduledClassesState>) { }

}
