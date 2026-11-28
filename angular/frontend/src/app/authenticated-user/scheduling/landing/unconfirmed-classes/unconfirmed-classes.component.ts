import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { 
  deletionModeForScheduledClassesActivated 
} from '../../classes-state/scheduled-classes.selectors';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../classes-state/scheduled-classes.reducers';
import { 
  ScheduledClassDeletionModeActivated, 
  ScheduledClassDeletionModeDeactivated 
} from '../../classes-state/scheduled-classes.actions';

@Component({
  selector: 'app-unconfirmed-classes',
  standalone: false,
  templateUrl: './unconfirmed-classes.component.html',
  styleUrl: './unconfirmed-classes.component.css'
})
export class UnconfirmedClassesComponent {

  deletionModeForUnconfirmedClassesActivated$: Observable<boolean> = of(false);

  @Input() unconfirmedClasses: ScheduledClassModel[];

  constructor(
    private scheduledClassesStore: Store<ScheduledClassesState>,
  ) { }

  ngOnInit(): void {
    this.deletionModeForUnconfirmedClassesActivated$ = this.scheduledClassesStore.pipe(
      select(deletionModeForScheduledClassesActivated)
    );
  }

  onActivateUnconfirmedlassDeletionMode(): void {
    this.scheduledClassesStore.dispatch(
      new ScheduledClassDeletionModeActivated()
    );
  }

  onDeactivateUnconfirmedClassDeletionMode(): void {
    this.scheduledClassesStore.dispatch(
      new ScheduledClassDeletionModeDeactivated()
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }
}
