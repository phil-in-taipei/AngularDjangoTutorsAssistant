import { Component, OnInit, Input } from '@angular/core';
import { NgForm } from '@angular/forms';
import { AppState } from '../../../../../reducers';
import { select, Store } from '@ngrx/store';

import { 
  StudentOrClassConfirmationModificationResponse 
} from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { 
  StudentOrClassPurchasedHoursUpdated 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.actions';


@Component({
  selector: 'app-edit-class-status-response',
  standalone: false,
  templateUrl: './edit-class-status-response.component.html',
  styleUrl: './edit-class-status-response.component.css'
})
export class EditClassStatusResponseComponent {

  @Input() studentOrClassHoursUpdate: StudentOrClassConfirmationModificationResponse;

  constructor(
    private store: Store<StudentsOrClassesState>
  ) { }


}
