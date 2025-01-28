import { Component, OnInit, Input } from '@angular/core';

import { 
  StudentOrClassConfirmationModificationResponse 
} from 'src/app/models/student-or-class.model';


@Component({
  selector: 'app-edit-class-status-response',
  standalone: false,
  templateUrl: './edit-class-status-response.component.html',
  styleUrl: './edit-class-status-response.component.css'
})
export class EditClassStatusResponseComponent {

  @Input() studentOrClassModificationResponse: StudentOrClassConfirmationModificationResponse;

}
