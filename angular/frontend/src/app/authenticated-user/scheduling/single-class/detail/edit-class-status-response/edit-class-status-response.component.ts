import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { NgForm } from '@angular/forms';
import { AppState } from '../../../../../reducers';
import { select, Store } from '@ngrx/store';
import { 
  ModifyClassStatusResponse, ScheduledClassModel
 } from '../../../../../models/scheduled-class.model';


@Component({
  selector: 'app-edit-class-status-response',
  standalone: false,
  templateUrl: './edit-class-status-response.component.html',
  styleUrl: './edit-class-status-response.component.css'
})
export class EditClassStatusResponseComponent {

}
