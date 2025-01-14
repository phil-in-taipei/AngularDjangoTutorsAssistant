import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { Observable, map } from "rxjs";
import {select, Store } from '@ngrx/store';

import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  ScheduledClassesMessagesCleared 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  scheduledClassesErrorMsg, 
  scheduledClassesSuccessMsg, 
  selectScheduledClassById 
} from '../../../classes-state/scheduled-classes.selectors';

@Component({
  selector: 'app-single-class-info',
  standalone: false,
  templateUrl: './single-class-info.component.html',
  styleUrl: './single-class-info.component.css'
})
export class SingleClassInfoComponent implements OnInit{

  classSubmitErrMsg$: Observable<string | undefined>;
  classSubmitSuccess$: Observable<string | undefined>;
  editStatusFormVisible: boolean = false;
  idFromRouteData:number;
  rescheduleFormVisible: boolean = false;
  scheduledClass$: Observable<ScheduledClassModel | undefined>;

  constructor(
    private route: ActivatedRoute, 
    private store: Store<ScheduledClassesState>
  ) { }

  ngOnInit(): void {
    this.store.dispatch(new ScheduledClassesMessagesCleared());
    this.idFromRouteData = +this.route.snapshot.params['id'];
    this.scheduledClass$ = this.store.pipe(select(
      selectScheduledClassById(this.idFromRouteData)
    ));
  }

  onClearStatusMsgs() {
    this.store.dispatch(new ScheduledClassesMessagesCleared());
  }

  toggleRescheduleForm() {
    if (this.rescheduleFormVisible) {
      this.rescheduleFormVisible = false;
    } else {
      this.rescheduleFormVisible = true;
      this.editStatusFormVisible = false;
    }
  }

  toggleEditStatusForm() {
    if (this.editStatusFormVisible) {
      this.editStatusFormVisible = false;
    } else {
      this.editStatusFormVisible = true;
      this.rescheduleFormVisible = false;
    }
  }

}
