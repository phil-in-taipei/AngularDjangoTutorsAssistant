import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from "rxjs";
import { select, Store } from '@ngrx/store';

import { deletionModeForScheduledClassesActivated } from '../../classes-state/scheduled-classes.selectors';
import { ScheduledClassDeletionRequested } from '../../classes-state/scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../classes-state/scheduled-classes.reducers';


@Component({
  selector: 'app-unconfirmed-class',
  standalone: false,
  templateUrl: './unconfirmed-class.component.html',
  styleUrl: './unconfirmed-class.component.css'
})
export class UnconfirmedClassComponent {

  @Input() unconfirmedClass: ScheduledClassModel;
  delModeActivated$: Observable<boolean> = of(false);
  delPopupVisible: boolean = false;
  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.delModeActivated$ = this.store.pipe(
      select(deletionModeForScheduledClassesActivated)
    );
  }

  showDelPU() {
    this.delPopupVisible = true;
  }

  hideDelPU() {
    this.delPopupVisible = false;
  }

  onUnconfirmedClassDeletion() {
    const payload = { id: this.unconfirmedClass.id };
    this.store.dispatch(
      new ScheduledClassDeletionRequested(payload)
    );
  }
}
