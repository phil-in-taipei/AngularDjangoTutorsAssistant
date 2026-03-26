import { Component, Input, EventEmitter, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

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
  @Output() closeFormEvent = new EventEmitter<boolean>();

  constructor(
    private store: Store<ScheduledClassesState>
  ) { }

}
